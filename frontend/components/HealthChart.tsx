'use client';

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { HealthSnapshot } from '@/lib/api';

interface HealthChartProps {
  data: HealthSnapshot[];
}

export default function HealthChart({ data }: HealthChartProps) {
  if (!data || data.length === 0) {
    return (
      <div className="h-64 flex items-center justify-center text-gray-400">
        No health data available
      </div>
    );
  }

  const chartData = [...data].reverse().map(snapshot => ({
    time: new Date(snapshot.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    health: snapshot.health_score,
    winRate: snapshot.win_rate * 100,
    drawdown: snapshot.current_drawdown_pct,
  }));

  return (
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis 
            dataKey="time" 
            tick={{ fontSize: 12 }}
            stroke="#9ca3af"
          />
          <YAxis 
            domain={[0, 100]}
            tick={{ fontSize: 12 }}
            stroke="#9ca3af"
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: 'white', 
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              fontSize: '12px'
            }}
          />
          <ReferenceLine y={75} stroke="#22c55e" strokeDasharray="3 3" />
          <ReferenceLine y={50} stroke="#f59e0b" strokeDasharray="3 3" />
          <Line 
            type="monotone" 
            dataKey="health" 
            stroke="#3b82f6" 
            strokeWidth={2}
            dot={false}
            name="Health Score"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
