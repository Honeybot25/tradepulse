import { useState } from 'react';
import { createStrategy, CreateStrategyData } from '@/lib/api';

interface CreateStrategyModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export default function CreateStrategyModal({ isOpen, onClose, onSuccess }: CreateStrategyModalProps) {
  const [formData, setFormData] = useState<CreateStrategyData>({
    name: '',
    type: 'custom',
    max_drawdown_threshold: 10,
    max_consecutive_losses_threshold: 5,
    discord_webhook_url: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [createdStrategy, setCreatedStrategy] = useState<any>(null);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const strategy = await createStrategy(formData);
      setCreatedStrategy(strategy);
      onSuccess();
    } catch (err) {
      setError('Failed to create strategy. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setCreatedStrategy(null);
    setFormData({
      name: '',
      type: 'custom',
      max_drawdown_threshold: 10,
      max_consecutive_losses_threshold: 5,
      discord_webhook_url: '',
    });
    onClose();
  };

  const copyWebhookUrl = () => {
    if (createdStrategy?.webhook_token) {
      const url = `http://localhost:8001/api/v1/webhooks/tradingview?token=${createdStrategy.webhook_token}`;
      navigator.clipboard.writeText(url);
      alert('Webhook URL copied to clipboard!');
    }
  };

  if (createdStrategy) {
    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div className="bg-white rounded-xl shadow-xl max-w-lg w-full p-6">
          <div className="text-center mb-6">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-gray-900">Strategy Created!</h2>
            <p className="text-gray-500 mt-1">{createdStrategy.name} is ready to receive signals.</p>
          </div>

          <div className="bg-gray-50 rounded-lg p-4 mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">Your TradingView Webhook URL</label>
            <div className="flex gap-2">
              <code className="flex-1 bg-white border rounded px-3 py-2 text-xs text-gray-600 overflow-x-auto">
                http://localhost:8001/api/v1/webhooks/tradingview?token={createdStrategy.webhook_token}
              </code>
              <button
                onClick={copyWebhookUrl}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition text-sm font-medium whitespace-nowrap"
              >
                Copy
              </button>
            </div>
            <p className="text-xs text-gray-500 mt-2">
              Paste this URL into your TradingView alert webhook settings.
            </p>
          </div>

          <div className="space-y-3">
            <button
              onClick={handleClose}
              className="w-full px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium"
            >
              Done
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-xl max-w-lg w-full p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold text-gray-900">Create New Strategy</h2>
          <button onClick={handleClose} className="text-gray-400 hover:text-gray-600">
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Strategy Name</label>
            <input
              type="text"
              required
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="e.g., Momentum Long"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Strategy Type</label>
            <select
              value={formData.type}
              onChange={(e) => setFormData({ ...formData, type: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="custom">Custom</option>
              <option value="momentum">Momentum</option>
              <option value="mean_reversion">Mean Reversion</option>
              <option value="breakout">Breakout</option>
              <option value="vwap">VWAP</option>
            </select>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Max Drawdown Alert (%)
              </label>
              <input
                type="number"
                min="1"
                max="50"
                value={formData.max_drawdown_threshold}
                onChange={(e) => setFormData({ ...formData, max_drawdown_threshold: parseFloat(e.target.value) })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Max Consecutive Losses
              </label>
              <input
                type="number"
                min="1"
                max="20"
                value={formData.max_consecutive_losses_threshold}
                onChange={(e) => setFormData({ ...formData, max_consecutive_losses_threshold: parseInt(e.target.value) })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Discord Webhook URL (Optional)
            </label>
            <input
              type="url"
              value={formData.discord_webhook_url}
              onChange={(e) => setFormData({ ...formData, discord_webhook_url: e.target.value })}
              placeholder="https://discord.com/api/webhooks/..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
            <p className="text-xs text-gray-500 mt-1">
              Get alerts when your strategy health degrades.
            </p>
          </div>

          <div className="pt-4">
            <button
              type="submit"
              disabled={loading}
              className="w-full px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Creating...' : 'Create Strategy'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
