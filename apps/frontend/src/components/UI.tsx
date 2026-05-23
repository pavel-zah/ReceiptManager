import React from 'react';
import { colors, spacing, typography, borderRadius } from '@/styles/theme';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  fullWidth?: boolean;
  loading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  fullWidth = false,
  loading = false,
  children,
  disabled,
  ...props
}) => {
  const baseStyles: React.CSSProperties = {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.sm,
    fontWeight: 600,
    borderRadius: '50px',
    border: 'none',
    outline: 'none',
    transition: 'all 0.2s ease',
    width: fullWidth ? '100%' : 'auto',
    opacity: disabled ? 0.5 : 1,
    cursor: disabled ? 'not-allowed' : 'pointer',
    letterSpacing: '0.01em',
    WebkitTapHighlightColor: 'transparent',
  };

  const variantStyles: Record<string, React.CSSProperties> = {
    primary: {
      backgroundColor: colors.primary,
      color: '#ffffff',
    },
    secondary: {
      backgroundColor: colors.secondaryBg,
      color: colors.text,
    },
    danger: {
      backgroundColor: colors.error,
      color: '#ffffff',
    },
    ghost: {
      backgroundColor: 'transparent',
      color: colors.primary,
      border: `1.5px solid ${colors.primary}`,
    },
  };

  const sizeStyles: Record<string, React.CSSProperties> = {
    sm: {
      ...typography.bodySmall,
      padding: `${spacing.sm}px ${spacing.md}px`,
    },
    md: {
      ...typography.body,
      padding: `${spacing.md}px ${spacing.lg}px`,
    },
    lg: {
      ...typography.subtitle,
      padding: `${spacing.lg}px ${spacing.xl}px`,
    },
  };

  return (
    <button
      style={{
        ...baseStyles,
        ...variantStyles[variant],
        ...sizeStyles[size],
      }}
      disabled={disabled || loading}
      {...props}
    >
      {loading && <span>⏳</span>}
      {children}
    </button>
  );
};

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  elevated?: boolean;
}

export const Card: React.FC<CardProps> = ({ elevated = false, children, style, ...props }) => (
  <div
    style={{
      backgroundColor: '#ffffff',
      borderRadius: borderRadius.lg,
      padding: spacing.lg,
      boxShadow: elevated ? `0 4px 20px ${colors.shadow}` : `0 1px 4px ${colors.shadow}`,
      border: `1px solid ${colors.divider}`,
      ...style,
    }}
    {...props}
  >
    {children}
  </div>
);

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input: React.FC<InputProps> = ({ label, error, style, ...props }) => (
  <div style={{ display: 'flex', flexDirection: 'column', gap: spacing.sm }}>
    {label && (
      <label style={{ ...typography.body, fontWeight: 500, color: colors.text }}>
        {label}
      </label>
    )}
    <input
      style={{
        ...typography.body,
        padding: `${spacing.md}px ${spacing.md}px`,
        borderRadius: borderRadius.sm,
        border: `1px solid ${error ? colors.error : colors.border}`,
        backgroundColor: colors.background,
        ...style,
      }}
      {...props}
    />
    {error && (
      <span style={{ ...typography.caption, color: colors.error }}>
        {error}
      </span>
    )}
  </div>
);

interface LoadingProps {
  fullScreen?: boolean;
}

export const Loading: React.FC<LoadingProps> = ({ fullScreen = false }) => (
  <div
    style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      height: fullScreen ? '100vh' : '200px',
      gap: spacing.md,
    }}
  >
    <div
      style={{
        width: '40px',
        height: '40px',
        border: `3px solid ${colors.border}`,
        borderTop: `3px solid ${colors.primary}`,
        borderRadius: '50%',
        animation: 'spin 1s linear infinite',
      }}
    />
    <span style={typography.body}>Загрузка...</span>
  </div>
);

interface ErrorAlertProps {
  message: string;
  onDismiss?: () => void;
}

export const ErrorAlert: React.FC<ErrorAlertProps> = ({ message, onDismiss }) => (
  <div
    style={{
      backgroundColor: '#ffebee',
      color: colors.error,
      padding: spacing.lg,
      borderRadius: borderRadius.md,
      border: `1px solid ${colors.error}`,
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      gap: spacing.md,
    }}
  >
    <span style={typography.body}>{message}</span>
    {onDismiss && (
      <button
        onClick={onDismiss}
        style={{
          background: 'none',
          color: colors.error,
          fontSize: '20px',
          cursor: 'pointer',
        }}
      >
        ✕
      </button>
    )}
  </div>
);

interface HeaderProps {
  title: string;
  onBack?: () => void;
  rightAction?: React.ReactNode;
}

export const Header: React.FC<HeaderProps> = ({ title, onBack, rightAction }) => (
  <div
    style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      borderBottom: `1px solid ${colors.divider}`,
      padding: `${spacing.md}px ${spacing.lg}px`,
      backgroundColor: colors.background,
    }}
  >
    {onBack && (
      <button
        onClick={onBack}
        style={{
          background: 'none',
          fontSize: '24px',
          cursor: 'pointer',
          color: colors.primary,
        }}
      >
        ←
      </button>
    )}
    <h1 style={{ ...typography.heading, flex: 1, margin: 0, marginLeft: onBack ? spacing.md : 0 }}>
      {title}
    </h1>
    {rightAction && <div>{rightAction}</div>}
  </div>
);

export const PageContainer: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div
    style={{
      display: 'flex',
      flexDirection: 'column',
      height: '100vh',
      backgroundColor: colors.background,
      overflow: 'hidden',
    }}
  >
    {children}
  </div>
);

export const PageContent: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div
    style={{
      flex: 1,
      overflowY: 'auto',
      padding: spacing.lg,
      display: 'flex',
      flexDirection: 'column',
      gap: spacing.lg,
    }}
  >
    {children}
  </div>
);

export const PageFooter: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div
    style={{
      padding: spacing.lg,
      backgroundColor: colors.background,
      borderTop: `1px solid ${colors.divider}`,
    }}
  >
    {children}
  </div>
);
