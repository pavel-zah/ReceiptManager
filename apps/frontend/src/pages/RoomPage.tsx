import React, { useState, useRef, useCallback } from 'react';
import { colors, spacing, typography, borderRadius } from '@/styles/theme';
import {
  Header,
  ErrorAlert,
} from '@/components/UI';
import { useAppStore } from '@/hooks/useAppStore';
import { hapticFeedback } from '@/utils/telegram';

const ASR_URL = 'http://localhost:8000/api/asr/transcribe';

type RecordingState = 'idle' | 'recording' | 'uploading';

export const RoomPage: React.FC = () => {
  const { setCurrentPage, currentRoom } = useAppStore();

  const [textInput, setTextInput] = useState('');
  const [recordingState, setRecordingState] = useState<RecordingState>('idle');
  const [recordingSeconds, setRecordingSeconds] = useState(0);
  const [transcription, setTranscription] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const inputRef = useRef<HTMLInputElement | null>(null);

  const startRecording = useCallback(async () => {
    try {
      setError(null);
      setTranscription(null);
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

      const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
        ? 'audio/webm;codecs=opus'
        : MediaRecorder.isTypeSupported('audio/webm')
        ? 'audio/webm'
        : 'audio/ogg';

      const recorder = new MediaRecorder(stream, { mimeType });
      chunksRef.current = [];

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };

      recorder.onstop = async () => {
        stream.getTracks().forEach((t) => t.stop());
        const audioBlob = new Blob(chunksRef.current, { type: mimeType });
        await sendToASR(audioBlob, mimeType);
      };

      recorder.start(250);
      mediaRecorderRef.current = recorder;
      setRecordingState('recording');
      setRecordingSeconds(0);

      timerRef.current = setInterval(() => {
        setRecordingSeconds((s) => s + 1);
      }, 1000);

      hapticFeedback('impact');
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Нет доступа к микрофону';
      setError(msg);
    }
  }, []);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
    }
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
    setRecordingState('uploading');
    hapticFeedback('success');
  }, []);

  const handleMicToggle = () => {
    if (recordingState === 'recording') stopRecording();
    else if (recordingState === 'idle') startRecording();
  };

  const handleSendText = () => {
    if (!textInput.trim()) return;
    console.log('[Room] Текстовый запрос:', textInput);
    setCurrentPage('select-items');
  };

  const sendToASR = async (blob: Blob, mimeType: string) => {
    try {
      const ext = mimeType.includes('ogg') ? 'ogg' : 'webm';
      const formData = new FormData();
      formData.append('file', blob, `recording.${ext}`);

      console.log('[ASR] Отправка аудио на сервер...', { size: blob.size, type: mimeType });

      const response = await fetch(ASR_URL, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      const result = await response.json();
      console.log('[ASR] Результат:', result);

      const text: string =
        result?.text ?? result?.transcription ?? result?.result ?? JSON.stringify(result);
      setTranscription(text);
      setTextInput((prev) => (prev ? prev + ' ' + text : text));
      hapticFeedback('success');
    } catch (err) {
      console.error('[ASR] Ошибка:', err);
      setError(err instanceof Error ? err.message : 'Ошибка распознавания');
      hapticFeedback('impact');
    } finally {
      setRecordingState('idle');
    }
  };

  const formatTime = (secs: number) => {
    const m = Math.floor(secs / 60).toString().padStart(2, '0');
    const s = (secs % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  };

  const roomCode = currentRoom?.shareCode ?? currentRoom?.id?.slice(0, 6).toUpperCase() ?? '------';
  const isRecording = recordingState === 'recording';
  const isUploading = recordingState === 'uploading';

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', backgroundColor: colors.background }}>
      <Header title="Комната" onBack={() => setCurrentPage('home')} />

      {/* Scrollable content */}
      <div style={{ flex: 1, overflowY: 'auto', padding: spacing.lg, display: 'flex', flexDirection: 'column', gap: spacing.md }}>
        {error && <ErrorAlert message={error} onDismiss={() => setError(null)} />}

        {/* Room code */}
        <div
          style={{
            background: `linear-gradient(135deg, ${colors.primary} 0%, ${colors.primaryDark} 100%)`,
            borderRadius: borderRadius.lg,
            padding: spacing.lg,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <div>
            <div style={{ ...typography.bodySmall, color: 'rgba(255,255,255,0.75)', marginBottom: 4 }}>
              Код комнаты
            </div>
            <div style={{ fontFamily: 'monospace', fontSize: '28px', fontWeight: 700, letterSpacing: '0.14em', color: '#ffffff' }}>
              {roomCode}
            </div>
          </div>
          <div style={{ fontSize: '36px' }}>🔒</div>
        </div>

        {/* Transcription result hint */}
        {transcription && (
          <div
            style={{
              backgroundColor: colors.pastelPeach,
              borderRadius: borderRadius.md,
              padding: `${spacing.sm}px ${spacing.md}px`,
              ...typography.bodySmall,
              color: colors.textSecondary,
              fontStyle: 'italic',
            }}
          >
            🎙 Распознано: «{transcription}»
          </div>
        )}

        {/* Recording indicator */}
        {isRecording && (
          <div
            style={{
              backgroundColor: '#FFE4E0',
              borderRadius: borderRadius.md,
              padding: `${spacing.sm}px ${spacing.md}px`,
              display: 'flex',
              alignItems: 'center',
              gap: spacing.sm,
            }}
          >
            <div
              style={{
                width: 10,
                height: 10,
                borderRadius: '50%',
                backgroundColor: colors.error,
                boxShadow: `0 0 0 4px rgba(232,107,107,0.25)`,
                flexShrink: 0,
              }}
            />
            <span style={{ ...typography.body, color: colors.error, fontWeight: 600 }}>
              Запись {formatTime(recordingSeconds)}
            </span>
          </div>
        )}

        {isUploading && (
          <div
            style={{
              backgroundColor: colors.pastelYellow,
              borderRadius: borderRadius.md,
              padding: `${spacing.sm}px ${spacing.md}px`,
              ...typography.body,
              color: colors.textSecondary,
            }}
          >
            ⏳ Распознаём речь...
          </div>
        )}

        {/* Manual selection */}
        <div
          style={{
            backgroundColor: colors.secondaryBg,
            borderRadius: borderRadius.lg,
            padding: spacing.lg,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            cursor: 'pointer',
            border: `1px solid ${colors.divider}`,
          }}
          onClick={() => setCurrentPage('select-items')}
        >
          <div>
            <div style={{ ...typography.subtitle, color: colors.text, marginBottom: 4 }}>
              Выбрать вручную
            </div>
            <div style={{ ...typography.bodySmall, color: colors.textSecondary }}>
              Отметьте позиции из чека
            </div>
          </div>
          <div style={{ fontSize: '22px', color: colors.primary }}>→</div>
        </div>
      </div>

      {/* Bottom chat bar */}
      <div
        style={{
          padding: `${spacing.sm}px ${spacing.md}px`,
          backgroundColor: '#ffffff',
          borderTop: `1px solid ${colors.divider}`,
          display: 'flex',
          alignItems: 'center',
          gap: spacing.sm,
          paddingBottom: `max(${spacing.md}px, env(safe-area-inset-bottom))`,
        }}
      >
        <input
          ref={inputRef}
          type="text"
          placeholder={isRecording ? 'Идёт запись...' : 'Что вы заказывали?'}
          value={isRecording ? '' : textInput}
          onChange={(e) => !isRecording && setTextInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSendText()}
          disabled={isRecording || isUploading}
          style={{
            flex: 1,
            height: '42px',
            borderRadius: '21px',
            border: `1.5px solid ${isRecording ? colors.error : colors.border}`,
            backgroundColor: isRecording ? '#FFF0EE' : colors.secondaryBg,
            padding: `0 ${spacing.md}px`,
            ...typography.body,
            color: colors.text,
            outline: 'none',
            transition: 'border-color 0.2s',
          }}
        />

        {/* Send button — shown only when text is ready */}
        {textInput.trim() && !isRecording && !isUploading && (
          <button
            onClick={handleSendText}
            style={{
              width: '42px', height: '42px', borderRadius: '50%',
              border: 'none', outline: 'none', cursor: 'pointer',
              backgroundColor: colors.primary, color: '#fff',
              fontSize: '18px', display: 'flex', alignItems: 'center',
              justifyContent: 'center', flexShrink: 0,
              boxShadow: `0 2px 8px ${colors.shadow}`,
            }}
            aria-label="Отправить"
          >
            →
          </button>
        )}

        {/* Mic button */}
        <button
          onClick={handleMicToggle}
          disabled={isUploading}
          style={{
            width: '42px', height: '42px', borderRadius: '50%',
            border: 'none', outline: 'none',
            cursor: isUploading ? 'not-allowed' : 'pointer',
            backgroundColor: isRecording ? colors.error : colors.primary,
            color: '#fff', fontSize: '20px',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            flexShrink: 0,
            boxShadow: isRecording ? `0 0 0 5px rgba(232,107,107,0.25)` : `0 2px 8px ${colors.shadow}`,
            transition: 'all 0.2s ease',
          }}
          aria-label={isRecording ? 'Остановить запись' : 'Голосовой ввод'}
        >
          {isUploading ? '⏳' : isRecording ? '⏹' : '🎙'}
        </button>
      </div>
    </div>
  );
};
