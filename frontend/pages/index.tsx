"""
Main dashboard page.
"""
import { useEffect, useState } from 'react';
import { getStrategies, Strategy } from '@/lib/api';
import StrategyCard from '@/components/StrategyCard';

export default function Dashboard() {
  const [strategies, setStrategies] = useState<Strategy[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadStrategies();
    // Auto-refresh every 30 seconds
    const interval = setInterval(loadStrategies, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadStrategies = async () => {
    try {
      const data = await getStrategies();
      setStrategies(data);
      setError(null);
    } catch (err) {
      setError('Failed to load strategies. Is the backend running?');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getSummaryStats = () => {
    const total = strategies.length;
    const healthy = strategies.filter(s => s.health_status === 'green').length;
    const warning = strategies.filter(s => s.health_status === 'yellow').length;
    const critical = strategies.filter(s => s.health_status === 'red').length;
    return { total, healthy, warning, critical };
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading TradePulse...</p>
        </div>
      </div>
    );
  }

  const stats = getSummaryStats();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">TradePulse</h1>
              <p className="text-sm text-gray-500 mt-1">AI Strategy Health Dashboard</p>
            </div>
            <div className="flex gap-3">
              <button
                onClick={loadStrategies}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition font-medium"
              >
                Refresh
              </button>
              <button
                onClick={() => alert('Strategy creation coming soon!')}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium"
              >
                + New Strategy
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {/* Error Banner */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            {error}
          </div>
        )}

        {/* Summary Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-xl shadow-sm border p-6">
            <div className="text-sm text-gray-500 font-medium uppercase tracking-wide">Strategies</div>
            <div className="text-3xl font-bold text-gray-900 mt-2">{stats.total}</div>
          </div>
          <div className="bg-white rounded-xl shadow-sm border p-6">
            <div className="text-sm text-green-600 font-medium uppercase tracking-wide">Healthy</div>
            <div className="text-3xl font-bold text-green-600 mt-2">{stats.healthy}</div>
          </div>
          <div className="bg-white rounded-xl shadow-sm border p-6">
            <div className="text-sm text-yellow-600 font-medium uppercase tracking-wide">Warning</div>
            <div className="text-3xl font-bold text-yellow-600 mt-2">{stats.warning}</div>
          </div>
          <div className="bg-white rounded-xl shadow-sm border p-6">
            <div className="text-sm text-red-600 font-medium uppercase tracking-wide">Critical</div>
            <div className="text-3xl font-bold text-red-600 mt-2">{stats.critical}</div>
          </div>
        </div>

        {/* Strategies Grid */}
        <div>
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Your Strategies</h2>
          {strategies.length === 0 ? (
            <div className="bg-white rounded-xl shadow-sm border p-12 text-center">
              <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No strategies yet</h3>
              <p className="text-gray-500 mb-6 max-w-md mx-auto">
                Create your first strategy to start monitoring your TradingView alerts in real-time.
              </p>
              <button
                onClick={() => alert('Strategy creation coming soon!')}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium"
              >
                Create Your First Strategy
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {strategies.map((strategy) => (
                <StrategyCard key={strategy.id} strategy={strategy} />
              ))}
            </div>
          )}
        </div>

        {/* Webhook URL Display */}
        {strategies.length > 0 && (
          <div className="mt-12 p-6 bg-blue-50 border border-blue-200 rounded-xl">
            <h3 className="text-sm font-semibold text-blue-900 mb-2">TradingView Integration</h3>
            <p className="text-sm text-blue-700 mb-3">
              Copy the webhook URL from each strategy card and paste it into your TradingView alert messages.
            </p>
            <div className="bg-white rounded-lg p-3 font-mono text-xs text-gray-600 overflow-x-auto">
              POST http://localhost:8000/api/v1/webhooks/tradingview?token=YOUR_WEBHOOK_TOKEN
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
