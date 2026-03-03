import { useEffect, useState } from 'react';
import { getStrategies, getCurrentHealth, Strategy, HealthSnapshot } from '@/lib/api';
import StrategyCard from '@/components/StrategyCard';
import HealthChart from '@/components/HealthChart';

export default function Dashboard() {
  const [strategies, setStrategies] = useState<Strategy[]>([]);
  const [healthData, setHealthData] = useState<Record<number, any>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 30000); // Refresh every 30s
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      const strategiesData = await getStrategies();
      setStrategies(strategiesData);

      // Load health for each strategy
      const healthPromises = strategiesData.map(s => getCurrentHealth(s.id));
      const healthResults = await Promise.allSettled(healthPromises);
      
      const healthMap: Record<number, any> = {};
      strategiesData.forEach((s, i) => {
        if (healthResults[i].status === 'fulfilled') {
          healthMap[s.id] = (healthResults[i] as PromiseFulfilledResult<any>).value;
        }
      });
      setHealthData(healthMap);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getHealthColor = (score: number) => {
    if (score >= 75) return 'text-green-500';
    if (score >= 50) return 'text-yellow-500';
    return 'text-red-500';
  };

  const getHealthBg = (score: number) => {
    if (score >= 75) return 'bg-green-100 border-green-300';
    if (score >= 50) return 'bg-yellow-100 border-yellow-300';
    return 'bg-red-100 border-red-300';
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl font-semibold">Loading TradePulse...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">TradePulse</h1>
              <p className="text-sm text-gray-500">AI Strategy Health Dashboard</p>
            </div>
            <button 
              onClick={loadData}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              Refresh
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-sm text-gray-500 mb-1">Total Strategies</div>
            <div className="text-3xl font-bold">{strategies.length}</div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-sm text-gray-500 mb-1">Healthy</div>
            <div className="text-3xl font-bold text-green-600">
              {strategies.filter(s => s.health_score >= 75).length}
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-sm text-gray-500 mb-1">Warning</div>
            <div className="text-3xl font-bold text-yellow-600">
              {strategies.filter(s => s.health_score >= 50 && s.health_score < 75).length}
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-sm text-gray-500 mb-1">Critical</div>
            <div className="text-3xl font-bold text-red-600">
              {strategies.filter(s => s.health_score < 50).length}
            </div>
          </div>
        </div>

        {/* Strategy Grid */}
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Your Strategies</h2>
          {strategies.length === 0 ? (
            <div className="bg-white rounded-lg shadow p-12 text-center">
              <div className="text-gray-400 mb-4">
                <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <p className="text-gray-500 mb-4">No strategies yet.</p>
              <p className="text-sm text-gray-400">
                Create a strategy and connect your TradingView alerts to get started.
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {strategies.map(strategy => (
                <StrategyCard 
                  key={strategy.id} 
                  strategy={strategy} 
                  health={healthData[strategy.id]}
                />
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
