import axios from 'axios';
import { getTelegramInitData } from './telegram';
import type { Room, Receipt, PaymentSplit } from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add Telegram init data to all requests
api.interceptors.request.use((config) => {
  const initData = getTelegramInitData();
  if (initData) {
    config.headers['X-Telegram-Init-Data'] = initData;
  }
  return config;
});

// Room API
export const roomAPI = {
  create: async (receiptId: string): Promise<Room> => {
    const { data } = await api.post('/rooms', { receiptId });
    return data;
  },

  getById: async (roomId: string): Promise<Room> => {
    const { data } = await api.get(`/rooms/${roomId}`);
    return data;
  },

  addParticipant: async (roomId: string, userId: string): Promise<Room> => {
    const { data } = await api.post(`/rooms/${roomId}/participants`, { userId });
    return data;
  },

  removeParticipant: async (roomId: string, userId: string): Promise<void> => {
    await api.delete(`/rooms/${roomId}/participants/${userId}`);
  },

  assignItemToUser: async (roomId: string, itemId: string, userId: string, quantity: number): Promise<Room> => {
    const { data } = await api.post(`/rooms/${roomId}/items/${itemId}/assign`, { userId, quantity });
    return data;
  },

  finalize: async (roomId: string): Promise<PaymentSplit[]> => {
    const { data } = await api.post(`/rooms/${roomId}/finalize`);
    return data;
  },

  delete: async (roomId: string): Promise<void> => {
    await api.delete(`/rooms/${roomId}`);
  },

  findByCode: async (code: string): Promise<Room> => {
    const { data } = await api.get(`/rooms/code/${code}`);
    return data;
  },
};

// Receipt API
export const receiptAPI = {
  create: async (file: File): Promise<Receipt> => {
    const formData = new FormData();
    formData.append('file', file);
    const { data } = await api.post('/receipts', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return data;
  },

  getById: async (receiptId: string): Promise<Receipt> => {
    const { data } = await api.get(`/receipts/${receiptId}`);
    return data;
  },

  addItem: async (receiptId: string, name: string, price: number, quantity: number): Promise<Receipt> => {
    const { data } = await api.post(`/receipts/${receiptId}/items`, { name, price, quantity });
    return data;
  },

  updateItem: async (receiptId: string, itemId: string, name: string, price: number, quantity: number): Promise<Receipt> => {
    const { data } = await api.put(`/receipts/${receiptId}/items/${itemId}`, { name, price, quantity });
    return data;
  },

  removeItem: async (receiptId: string, itemId: string): Promise<Receipt> => {
    const { data } = await api.delete(`/receipts/${receiptId}/items/${itemId}`);
    return data;
  },

  updateTipAndService: async (receiptId: string, tip: number, service: number): Promise<Receipt> => {
    const { data } = await api.put(`/receipts/${receiptId}/tip-service`, { tip, service });
    return data;
  },
};

// User API
export const userAPI = {
  register: async (userId: string, username: string, firstName: string): Promise<{ id: string }> => {
    const { data } = await api.post('/users', { userId, username, firstName });
    return data;
  },

  getProfile: async (): Promise<{ id: string; username: string; firstName: string }> => {
    const { data } = await api.get('/users/me');
    return data;
  },
};

export default api;
