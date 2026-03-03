"""
API client for TradePulse.
"""
import axios from 'axios';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

const api = axios.create({
  baseURL: `${API_BASE}`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Strategy {
  id: number;
  name: string;
  type: string;
  status: 'active' | 'paused' | 'error';
  health_status: 'green' | 'yellow' | 'red';
  webhook_token: string;
  win_rate: number;
  max_drawdown: number;
  consecutive_losses: number;
  created_at: string;
  updated_at: string;
  last_signal_at: string | null;
  discord_webhook_url?: string;
}

export interface CreateStrategyData {
  name: string;
  type?: string;
  max_drawdown_threshold?: number;
  max_consecutive_losses_threshold?: number;
  discord_webhook_url?: string;
}

// API functions
export const getStrategies = async (): Promise<Strategy[]> => {
  const response = await api.get('/api/v1/strategies');
  return response.data;
};

export const getStrategy = async (id: number): Promise<Strategy> => {
  const response = await api.get(`/api/v1/strategies/${id}`);
  return response.data;
};

export const createStrategy = async (data: CreateStrategyData): Promise<Strategy> => {
  const response = await api.post('/api/v1/strategies', data);
  return response.data;
};

export const updateStrategy = async (id: number, status: string) => {
  const response = await api.patch(`/api/v1/strategies/${id}?status=${status}`);
  return response.data;
};

export const deleteStrategy = async (id: number) => {
  const response = await api.delete(`/api/v1/strategies/${id}`);
  return response.data;
};

// Health check
export const healthCheck = async () => {
  const response = await api.get('/api/v1/health');
  return response.data;
};
