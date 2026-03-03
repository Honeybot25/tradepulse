"""
Strategy card component for dashboard.
"""
import { Strategy } from '@/lib/api';

interface StrategyCardProps {
  strategy: Strategy;
}

export default function StrategyCard({ strategy }: StrategyCardProps) {
  const getHealthColor = (status: string) => {
    switch (status) {
      case 'green': return 'text-green-600';
      case 'yellow': return 'text-yellow-600';
      case 'red': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const getHealthBg = (status: string) => {
    switch (status) {
      case 'green': return 'bg-green-50 border-green-200';
      case 'yellow': return 'bg-yellow-50 border-yellow-200';
      case 'red': return 'bg-red-50 border-red-200';
      default: return 'bg-gray-50 border-gray-200';
    }
  };

  const getDotColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-500';
      case 'paused': return 'bg-yellow-500';
      case 'error': return 'bg-red-500';
      default: return 'bg-gray-400';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'green': return 'HEALTHY';
      case 'yellow': return 'WARNING';
      case 'red': return 'CRITICAL';
      default: return 'UNKNOWN';
    }
  };

  const getStatusBadgeColor = (status: string) => {
    switch (status) {
      case 'green': return 'bg-green-100 text-green-800';
      case 'yellow': return 'bg-yellow-100 text-yellow-800';
      case 'red': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  // Determine health score based on status
  const healthScore = strategy.health_status === 'green' ? 85 : 
                      strategy.health_status === 'yellow' ? 65 : 35;

  return (
    <div className={`rounded-lg border shadow-sm p-6 ${getHealthBg(strategy.health_status)}`}>
      <div className="flex justify-between items-start mb-4">
        <div>
          <div className="flex items-center gap-2">
            <h3 className="text-lg font-semibold text-gray-900">{strategy.name}</h3>
            <span className={`w-2 h-2 rounded-full ${getDotColor(strategy.status)}`} />
          </div>
          <p className="text-sm text-gray-500 capitalize">{strategy.type.replace('_', ' ')}</p>
        </div>
        <div className={`text-3xl font-bold ${getHealthColor(strategy.health_status)}`}>
          {healthScore}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <div className="bg-white/50 rounded p-3">
          <div className="text-xs text-gray-500 uppercase tracking-wide">Win Rate</div>
          <div className="text-xl font-semibold text-gray-800">
            {strategy.win_rate.toFixed(1)}%
          </div>
        </div>
        <div className="bg-white/50 rounded p-3">
          <div className="text-xs text-gray-500 uppercase tracking-wide">Drawdown</div>
          <div className="text-xl font-semibold text-gray-800">
            {strategy.max_drawdown.toFixed(1)}%
          </div>
        </div>
        <div className="bg-white/50 rounded p-3">
          <div className="text-xs text-gray-500 uppercase tracking-wide">Consec. Losses</div>
          <div className={`text-xl font-semibold ${strategy.consecutive_losses > 3 ? 'text-red-600' : 'text-gray-800'}`}>
            {strategy.consecutive_losses}
          </div>
        </div>
        <div className="bg-white/50 rounded p-3">
          <div className="text-xs text-gray-500 uppercase tracking-wide">Status</div>
          <div className="text-xl font-semibold text-gray-800 capitalize">
            {strategy.status}
          </div>
        </div>
      </div>

      <div className="flex justify-between items-center text-sm">
        <span className="text-gray-500">
          Last signal: {strategy.last_signal_at 
            ? new Date(strategy.last_signal_at).toLocaleTimeString() 
            : 'Never'}
        </span>
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusBadgeColor(strategy.health_status)}`}>
          {getStatusLabel(strategy.health_status)}
        </span>
      </div>

      {strategy.discord_webhook_url && (
        <div className="mt-3 flex items-center gap-1 text-xs text-gray-400">
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
            <path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03z"/>
          </svg>
          Discord alerts enabled
        </div>
      )}
    </div>
  );
}
