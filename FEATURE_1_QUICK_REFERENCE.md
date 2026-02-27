# Feature #1 Quick Reference Guide

## What Was Added

### 🎨 Visual Enhancements
- **Node Colors** - Indicate health status (red=critical, yellow=warning, green=healthy)
- **Edge Thickness** - Thicker lines = higher EPS throughput
- **Edge Colors** - Dark red (high), orange (medium), gold (medium-low), gray (low)
- **Metric Labels** - EPS displayed on nodes and edges

### 📊 New API Methods
```python
api_client.get_pipeline_status(group_id)      # Get pipeline metrics
api_client.get_source_health(group_id)        # Get input health
api_client.get_destination_health(group_id)   # Get output health
```

### 🔧 New Helper Functions
```python
_get_node_color(health_metrics)        # health → color
_get_edge_attributes(eps, max_eps)     # eps → styling
```

## How It Works

```
Health Data (error_rate, drop_rate)
         ↓
    _get_node_color()
         ↓
  Node fills with color (red/yellow/green)

Pipeline EPS
         ↓
  _get_edge_attributes()
         ↓
  Edge thickness & color (thick/dark = high volume)
```

## Color Legend

| Color | Health Status | Error Rate |
|-------|---|---|
| 🟢 Lightblue/green | Healthy | < 5% |
| 🟡 Lightyellow | Warning | 5-10% |
| 🔴 Lightcoral | Critical | > 10% |

## Edge Styling

| Color | EPS Relative Volume |
|-------|---|
| 🔴 Darkred | > 80% of max |
| 🟠 Orange | 50-80% of max |
| 🟡 Gold | 20-50% of max |
| ⚫ Gray | < 20% of max |

## Usage

**No changes needed to use the feature:**
```python
from cribl_api import get_cached_api_client
from graph_generator import generate_graph

api_client = get_cached_api_client()
dot = generate_graph(api_client)  # Now includes metrics!
svg = dot.pipe(format="svg").decode("utf-8")
```

## Environment Variables

None new - uses existing:
- `CRIBL_BASE_URL`
- `CRIBL_AUTH_TOKEN` (or username/password)

## Files Modified

| File | Purpose |
|------|---|
| `cribl_api.py` | Added 3 new API methods |
| `graph_generator.py` | Added 2 helper functions, enhanced main function |
| `tests/test_graph_generator.py` | 7 new test cases |
| `tests/test_cribl_api.py` | 4 new test cases |
| `docs/CODE_REFERENCE.md` | Updated API & graph generator docs |

## Testing

Run tests:
```bash
python -m pytest tests/test_graph_generator.py::TestGraphGenerator::test_generate_graph_with_health_status -v
python -m pytest tests/test_graph_generator.py::TestGraphGenerator::test_generate_graph_with_edge_metrics -v
python -m pytest tests/test_cribl_api.py -v
```

## Troubleshooting

**Q: I don't see health colors on nodes**
- A: The health API endpoint may not be available in your Cribl version. The app gracefully handles this and will show default colors.

**Q: Edges are all gray**
- A: The pipeline status endpoint may not be available. The app will show all edges as gray with minimum thickness.

**Q: Errors in console about health/pipeline endpoints**
- A: These are normal if your Cribl version doesn't have those endpoints. The app continues working.

## Performance Impact

- Minimal - adds ~7 API calls per graph generation
- No impact on rendering time (still Graphviz)
- Memory usage negligible (metrics only in memory during generation)

## Backward Compatibility

✅ Fully backward compatible
- Existing code continues to work unchanged
- Graceful degradation if APIs unavailable
- Visual-only enhancement (no breaking changes)

## Next Steps

1. ✅ Test with your Cribl instance
2. ✅ Adjust color thresholds if needed (see `_get_node_color()`)
3. ✅ Plan Feature #2: Configuration Analysis

---

For detailed documentation, see:
- `docs/FEATURE_1_METRICS_OVERLAY.md`
- `docs/CODE_REFERENCE.md`
- `IMPLEMENTATION_SUMMARY_FEATURE_1.md`
