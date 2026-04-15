# Run

```bash
cd frontend
npm install
npm run dev
```

Set backend URL if needed:

```bash
VITE_API_BASE=http://localhost:8000/api/v1 npm run dev
```

This UI includes:
- Heston simulation trigger wired to backend `/simulation/heston`
- terminal-style KPI strip
- multi-path chart, variance chart, and synthetic vol-surface grid
