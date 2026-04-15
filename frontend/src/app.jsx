import { useMemo, useState } from 'react';
import {
  Area,
  AreaChart,
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import Panel from './components/Panel';

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000/api/v1';

function generateSurfacePoints() {
  const maturities = [0.25, 0.5, 1, 1.5, 2];
  const moneyness = [0.8, 0.9, 1.0, 1.1, 1.2];
  return maturities.flatMap((t) =>
    moneyness.map((k) => ({
      t,
      k,
      iv: Number((0.17 + (1 - k) * 0.18 + 0.04 * Math.sqrt(t)).toFixed(3)),
    }))
  );
}

export default function App() {
  const [paths, setPaths] = useState([]);
  const [vols, setVols] = useState([]);
  const [loading, setLoading] = useState(false);

  const surface = useMemo(() => generateSurfacePoints(), []);

  const runSimulation = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/simulation/heston`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          S0: 100,
          v0: 0.04,
          rho: -0.65,
          T: 1,
          n_steps: 120,
          n_paths: 30,
          mu: 0.02,
          theta: 0.04,
          kappa: 1.8,
          xi: 0.35,
          seed: 7,
        }),
      });
      const data = await response.json();

      const sampled = Array.from({ length: data.St.length }, (_, i) => ({
        t: i,
        p1: data.St[i][0],
        p2: data.St[i][1],
        p3: data.St[i][2],
        v: data.vt[i][0],
      }));
      setPaths(sampled);
      setVols(sampled.map((x) => ({ t: x.t, v: x.v })));
    } finally {
      setLoading(false);
    }
  };

  const kpis = [
    ['Model', 'Heston + FFT + MC'],
    ['Status', loading ? 'Running…' : 'Ready'],
    ['API', API_BASE],
    ['Seed', '7'],
  ];

  return (
    <div className="terminal">
      <div className="topbar">HESTON VOL LAB // TERMINAL MODE</div>

      <div className="kpi-row">
        {kpis.map(([k, v]) => (
          <div key={k} className="kpi">
            <div className="kpi-key">{k}</div>
            <div className="kpi-val">{v}</div>
          </div>
        ))}
      </div>

      <div className="grid">
        <Panel
          title="Path Simulation"
          right={<button onClick={runSimulation}>{loading ? 'Running' : 'Run Scenario'}</button>}
        >
          <div className="chart-wrap">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={paths}>
                <CartesianGrid stroke="#1f2a33" />
                <XAxis dataKey="t" stroke="#6f8599" />
                <YAxis stroke="#6f8599" />
                <Tooltip />
                <Line type="monotone" dataKey="p1" stroke="#f7c948" dot={false} />
                <Line type="monotone" dataKey="p2" stroke="#4fd1c5" dot={false} />
                <Line type="monotone" dataKey="p3" stroke="#7aa2f7" dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Instantaneous Variance">
          <div className="chart-wrap">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={vols}>
                <CartesianGrid stroke="#1f2a33" />
                <XAxis dataKey="t" stroke="#6f8599" />
                <YAxis stroke="#6f8599" />
                <Tooltip />
                <Area type="monotone" dataKey="v" stroke="#ff6b6b" fill="#7f1d1d" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Synthetic Vol Surface (for desk preview)">
          <div className="surface-grid">
            {surface.map((pt) => (
              <div key={`${pt.t}-${pt.k}`} className="surface-cell">
                <span>T {pt.t}</span>
                <span>K/S {pt.k}</span>
                <strong>{(pt.iv * 100).toFixed(1)}%</strong>
              </div>
            ))}
          </div>
        </Panel>
      </div>
    </div>
  );
}