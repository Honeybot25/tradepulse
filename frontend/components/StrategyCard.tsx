import { Strategy } from '@/lib/api';

interface StrategyCardProps {
  strategy: Strategy;
  health: any;
}

export default function StrategyCard({ strategy, health }: StrategyCardProps) {
  const getHealthColor = (score: number) => {
    if (score >= 75) return 'text-green-600';
    if (score >= 50) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getHealthBg = (score: number) => {
    if (score >= 75) return 'bg-green-50 border-green-200';
    if (score >= 50) return 'bg-yellow-50 border-yellow-200';
    return 'bg-red-50 border-red-200';
  };

  const getDotColor = (status: string) => {
    if (status === 'active') return 'bg-green-500';
    if (status === 'paused') return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className={`rounded-lg border shadow-sm p-6 ${getHealthBg(strategy.health_score || 0)}`}>
      <div className="flex justify-between items-start mb-4">
        <div>
          <div className="flex items-center gap-2">
            <h3 className="text-lg font-semibold text-gray-900">{strategy.name}</h3>
            <span className={`w-2 h-2 rounded-full ${getDotColor(strategy.status)}`} />
          </div>
          <p className="text-sm text-gray-500 capitalize">{strategy.type.replace('_', ' ')}</p>
        </div>
        <div className={`text-3xl font-bold ${getHealthColor(strategy.health_score || 0)}`}>
          {Math.round(strategy.health_score || 0)}
        </div>
      </div>

      {health && (
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div className="bg-white/50 rounded p-3">
            <div className="text-xs text-gray-500 uppercase tracking-wide">Win Rate</div>
            <div className="text-xl font-semibold text-gray-800">
              {(health.win_rate * 100).toFixed(1)}%
            </div>
          </div>
          <div className="bg-white/50 rounded p-3">
            <div className="text-xs text-gray-500 uppercase tracking-wide">Drawdown</div>
            <div className="text-xl font-semibold text-gray-800">
              {health.current_drawdown_pct?.toFixed(2) || 0}%
            </div>
          </div>
          <div className="bg-white/50 rounded p-3">
            <div className="text-xs text-gray-500 uppercase tracking-wide">Signals</div>
            <div className="text-xl font-semibold text-gray-800">
              {health.total_signals}
            </div>
          </div>
          <div className="bg-white/50 rounded p-3">
            <div className="text-xs text-gray-500 uppercase tracking-wide">Consec. Losses</div>
            <div className={`text-xl font-semibold ${health.consecutive_losses > 2 ? 'text-red-600' : 'text-gray-800'}`}>
              {health.consecutive_losses}
            </div>
          </div>
        </div>
      )}

      <div className="flex justify-between items-center text-sm">
        <span className="text-gray-500">
          Last updated: {new Date(strategy.updated_at).toLocaleTimeString()}
        </span>
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
          strategy.health_score >= 75 ? 'bg-green-100 text-green-800' :
          strategy.health_score >= 50 ? 'bg-yellow-100 text-yellow-800' :
          'bg-red-100 text-red-800'
        }`}>
          {strategy.health_score >= 75 ? 'HEALTHY' :
           strategy.health_score >= 50 ? 'WARNING' : 'CRITICAL'}
        </span>
      </div>
    </div>
  );
}
