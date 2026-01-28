"use client";

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { TrendingUp, AlertTriangle, Activity, Search, BookOpen, ExternalLink } from 'lucide-react';
import clsx from 'clsx';

interface HistoricalDataPoint {
  year: number;
  revenue: number;
  net_income: number;
  operating_cash_flow: number;
}

interface Reference {
  title: string;
  url: string;
  context: string;
}

interface AnalysisResult {
  ticker: string;
  summary: string;
  details: string;
  metrics: { metric_name: string; value: number; unit: string; explanation: string }[];
  history: HistoricalDataPoint[];
  trends: { metric: string; trend: string; confidence: number; description: string }[];
  risks: { risk_category: string; description: string; severity: string }[];
  references: Reference[];
}

export default function Dashboard() {
  const [ticker, setTicker] = useState('');
  const [data, setData] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!ticker) return;
    setLoading(true);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/analyze/${ticker}`, {
        method: 'POST'
      });
      const result = await response.json();
      setData(result);
    } catch (error) {
      console.error("Failed to fetch analysis", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 z-0 opacity-40 pointer-events-none">
        <div className="absolute inset-0" style={{ 
          backgroundImage: 'radial-gradient(#cbd5e1 1px, transparent 1px)', 
          backgroundSize: '32px 32px' 
        }}></div>
      </div>
      
      {/* Abstract Gradient Blob */}
      <div className="absolute top-0 right-0 -mr-20 -mt-20 w-[600px] h-[600px] bg-blue-100/50 rounded-full blur-3xl pointer-events-none z-0"></div>
      <div className="absolute bottom-0 left-0 -ml-20 -mb-20 w-[500px] h-[500px] bg-emerald-100/50 rounded-full blur-3xl pointer-events-none z-0"></div>

      <div className="max-w-7xl mx-auto space-y-8 relative z-10 p-8">
        
        {/* Header Section */}
        <div className="flex flex-col md:flex-row justify-between items-center gap-6 bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-sm border border-slate-200/60">
          <div className="relative">
             <div className="absolute -left-4 -top-4 w-12 h-12 bg-blue-100 rounded-full blur-xl opacity-70"></div>
             <h1 className="text-4xl font-extrabold text-slate-900 flex items-center gap-3 relative z-10">
              <div className="p-2 bg-blue-600 rounded-lg text-white shadow-lg shadow-blue-600/20">
                <Activity className="h-8 w-8" />
              </div>
              AI Financial Analyst
            </h1>
            <p className="text-slate-500 mt-2 text-lg font-medium">Multi-agent financial insights & risk detection</p>
          </div>
          <div className="flex gap-3 w-full md:w-auto bg-slate-100/50 p-2 rounded-xl border border-slate-200">
            <input 
              type="text" 
              placeholder="Enter Ticker (e.g. AAPL, MSFT)" 
              className="px-4 py-3 bg-white border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 w-full md:w-80 shadow-sm text-lg"
              value={ticker}
              onChange={(e) => setTicker(e.target.value.toUpperCase())}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            />
            <button 
              onClick={handleSearch}
              disabled={loading}
              className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2 font-semibold transition-all shadow-md shadow-blue-600/20 hover:shadow-lg hover:shadow-blue-600/30"
            >
              {loading ? <Activity className="animate-spin h-5 w-5" /> : <Search className="h-5 w-5" />}
              Analyze
            </button>
          </div>
        </div>

        {data && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            {/* Main Content Area */}
            <div className="lg:col-span-2 space-y-6">
              
              {/* Executive Summary */}
              <Card className="bg-white shadow-sm border-slate-200">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-slate-800">
                    <BookOpen className="h-5 w-5 text-blue-600" />
                    Executive Summary
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-lg text-slate-700 leading-relaxed">{data.summary}</p>
                </CardContent>
              </Card>

              {/* Financial Charts */}
              <Card className="bg-white shadow-sm border-slate-200">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-slate-800">
                    <TrendingUp className="h-5 w-5 text-green-600" />
                    Financial Performance (5 Years)
                  </CardTitle>
                  <CardDescription>Revenue vs Net Income Trends</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="h-[300px] w-full mt-4">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={data.history}>
                        <XAxis dataKey="year" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                        <YAxis 
                          stroke="#64748b" 
                          fontSize={12} 
                          tickLine={false} 
                          axisLine={false}
                          tickFormatter={(value) => `$${value / 1000}B`}
                        />
                        <Tooltip 
                          contentStyle={{ backgroundColor: '#fff', borderRadius: '8px', border: '1px solid #e2e8f0' }}
                          formatter={(value: number) => [`$${value.toLocaleString()}`, '']}
                        />
                        <Legend wrapperStyle={{ paddingTop: '20px' }} />
                        <Bar dataKey="revenue" name="Revenue" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                        <Bar dataKey="net_income" name="Net Income" fill="#10b981" radius={[4, 4, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </CardContent>
              </Card>

              {/* Metrics Grid */}
              <div className="grid grid-cols-2 gap-4">
                {data.metrics.map((m, idx) => (
                  <Card key={idx} className="bg-white shadow-sm border-slate-200">
                    <CardHeader className="pb-2">
                      <CardDescription className="font-medium text-slate-500">{m.metric_name}</CardDescription>
                      <CardTitle className="text-2xl font-bold text-slate-900">
                        {m.unit === 'ratio' ? `${(m.value * 100).toFixed(1)}%` : m.value}
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-xs text-slate-500 leading-snug">{m.explanation}</p>
                    </CardContent>
                  </Card>
                ))}
              </div>

              {/* References Section */}
              <Card className="bg-slate-50 border-slate-200">
                <CardHeader className="pb-3">
                  <CardTitle className="text-sm font-semibold text-slate-500 uppercase tracking-wider">
                    Sources & References
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-3">
                    {data.references.map((ref, idx) => (
                      <li key={idx} className="flex items-start gap-3 text-sm">
                        <span className="mt-1 h-1.5 w-1.5 rounded-full bg-blue-400 shrink-0" />
                        <div>
                          <a href={ref.url} target="_blank" rel="noopener noreferrer" className="font-medium text-blue-600 hover:underline flex items-center gap-1">
                            {ref.title}
                            <ExternalLink className="h-3 w-3" />
                          </a>
                          <p className="text-slate-500 text-xs mt-0.5">Context: {ref.context}</p>
                        </div>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>

            </div>

            {/* Sidebar (Risk & Trends) */}
            <div className="space-y-6">
              
              {/* Risk Signals */}
              <Card className="h-fit border-l-4 border-l-amber-500 shadow-sm bg-white">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-slate-800">
                    <AlertTriangle className="h-5 w-5 text-amber-500" />
                    Risk Analysis
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {data.risks.map((r, idx) => (
                    <div key={idx} className="p-4 bg-amber-50 rounded-lg border border-amber-100">
                      <div className="flex justify-between items-start mb-2">
                        <h4 className="font-semibold text-amber-900 text-sm uppercase tracking-wide">{r.risk_category}</h4>
                        <Badge className={clsx(
                          "text-[10px] px-2 py-0.5",
                          r.severity === 'high' ? "bg-red-500 hover:bg-red-600" : 
                          r.severity === 'medium' ? "bg-amber-500 hover:bg-amber-600" : "bg-blue-500 hover:bg-blue-600"
                        )}>
                          {r.severity}
                        </Badge>
                      </div>
                      <p className="text-sm text-amber-800 leading-relaxed">
                        {r.description}
                      </p>
                    </div>
                  ))}
                </CardContent>
              </Card>

              {/* Key Trends List */}
              <Card className="bg-white shadow-sm border-slate-200">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-slate-800">
                    <TrendingUp className="h-5 w-5 text-blue-600" />
                    Market Signals
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {data.trends.map((t, idx) => (
                      <div key={idx} className="flex items-start gap-3 p-3 hover:bg-slate-50 rounded-lg transition-colors border border-transparent hover:border-slate-100">
                        <div className={clsx(
                          "p-1.5 rounded-full shrink-0 mt-0.5",
                          t.trend === 'up' ? "bg-green-100 text-green-600" : "bg-red-100 text-red-600"
                        )}>
                          {t.trend === 'up' ? <TrendingUp className="h-4 w-4" /> : <TrendingUp className="h-4 w-4 rotate-180" />}
                        </div>
                        <div>
                          <div className="flex items-center gap-2">
                            <h4 className="font-medium text-slate-900">{t.metric}</h4>
                            <span className="text-xs text-slate-400 bg-slate-100 px-1.5 rounded">
                              {(t.confidence * 100).toFixed(0)}% conf.
                            </span>
                          </div>
                          <p className="text-sm text-slate-600 mt-1">{t.description}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

            </div>
            
          </div>
        )}
      </div>
    </div>
  );
}
