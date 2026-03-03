import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Strategy {
  id: number;
  name: string;
  type: string;
  status: string;
  health_score: number;
  created_at: string;
  updated_at: string;
}

export interface HealthSnapshot {
  id: number;
  timestamp: string;
  total_signals: number;
  win_count: number;
  loss_count: number;
  win_rate: number;
  avg_pnl: number;
  current_drawdown_pct: number;
  consecutive_losses: number;
  health_score: number;
  health_status: 'green' | 'yellow' | 'red';
}

export const getStrategies = async (): Promise<Strategy[]> => {
  const response = await api.get('/strategies/');
  return response.data;
};

export const getStrategyHealth = async (id: number): Promise<HealthSnapshot[]> => {
  const response = await api.get(`/strategies/${id}/health`);
  return response.data;
};

export const getCurrentHealth = async (id: number) => {
  const response = await api.get(`/strategies/${id}/current-health`);
  return response.data;
};

export const createStrategy = async (data: {
  name: string;
  type?: string;
  max_drawdown_pct?: number;
  min_win_rate?: number;
  max_consecutive_losses?: number;
  alert_webhook_url?: string;
}): Promise<Strategy> => {
  const response = await api.post('/strategies/', data);
  return response.data;
};
