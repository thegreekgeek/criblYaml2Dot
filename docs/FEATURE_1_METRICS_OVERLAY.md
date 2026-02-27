# Feature #1: Observability and Metrics Overlay - Implementation Guide

## Overview

Feature #1 introduces comprehensive observability to the Cribl Pipeline Visualizer by overlaying real-time metrics and health status onto the pipeline graph. This allows teams to quickly identify bottlenecks, unhealthy components, and high-traffic paths at a glance.

## Implementation Status

**Current Status: 75% Complete** ✅

### What's Implemented

#### 1. **Live Traffic Indicators on Nodes** ✅
- **EPS (Events Per Second)** displayed directly on input and output nodes
- **Event count** as fallback metric when EPS unavailable
- **Real-time metrics** fetched from Cribl API status endpoints

**Example Node Label:**
```
in_syslog
(123.46 EPS)
------------
Syslog Input
```

#### 2. **Live Traffic Indicators on Edges** ✅ (NEW)
- **Pipeline-level EPS** shown on connection edges
- **Dynamic edge thickness** scales with traffic volume (penwidth: 1-5)
- **Dynamic edge coloring** indicates relative traffic intensity:
  - `darkred` - High volume (>80% of max)
  - `orange` - Medium-high volume (50-80%)
  - `gold` - Medium volume (20-50%)
  - `gray` - Low volume (<20%)

**Example Edge Rendering:**
```
in_syslog -> out_s3 [label="main\n(100.00 EPS)", color=orange, penwidth=3.5]
```

#### 3. **Health Status Color-Coding** ✅ (NEW)
- **Dynamic node coloring** based on health metrics
- **Error rate and drop rate** monitoring
- **Three-tier health status:**
  - 🟢 Healthy (error_rate < 5%) - Uses default colors (lightblue for inputs, lightgreen for outputs)
  - 🟡 Warning (5% ≤ error_rate < 10%) - `lightyellow`
  - 🔴 Critical (error_rate ≥ 10%) - `lightcoral` (red)

#### 4. **Graceful API Error Handling** ✅
- All metric API calls wrapped in try-catch
- Application continues rendering if metrics unavailable
- Detailed error logging for debugging
- Empty metric fallbacks ensure robustness

### What's Not Implemented

#### 1. **Byte Throughput Display** ❌ (Pending API Support)
- Requires API endpoint providing byte rate metrics
- Can be added when available: `get_bytes_per_sec()` on connections
- Currently using EPS as primary metric

#### 2. **Advanced Health Metrics** ❌ (Extensible)
- Queue depth monitoring
- Memory usage tracking
- CPU utilization visualization
- Can be added to health endpoints as they become available

## API Methods

### New Methods Added to `CriblAPI`

#### `get_pipeline_status(group_id)`
```python
"""
Retrieves status metrics for all pipelines in a worker group.
Returns: {"items": [{"id": "pipeline_name", "eps": 100.5, ...}]}
"""
```
- Endpoint: `/api/v1/m/{group_id}/system/status/pipelines`
- Returns pipeline-level metrics including EPS
- Gracefully handles missing endpoint (returns empty items)

#### `get_source_health(group_id)`
```python
"""
Retrieves health information for all input sources.
Returns: {"items": [{"id": "source_id", "error_rate": 2.5, "drop_rate": 0.0, ...}]}
"""
```
- Endpoint: `/api/v1/m/{group_id}/system/health/inputs`
- Returns error rates, drop rates, and other health metrics
- Gracefully handles missing endpoint

#### `get_destination_health(group_id)`
```python
"""
Retrieves health information for all output destinations.
Returns: {"items": [{"id": "dest_id", "error_rate": 1.0, ...}]}
"""
```
- Endpoint: `/api/v1/m/{group_id}/system/health/outputs`
- Returns destination health metrics
- Gracefully handles missing endpoint

### Updated Methods

#### `generate_graph(api_client)`
Enhanced to:
1. Fetch all metric sources (status + health)
2. Calculate max EPS for edge scaling normalization
3. Apply dynamic node coloring based on health
4. Apply dynamic edge styling based on throughput
5. Include pipeline metrics in edge labels

## Helper Functions

### `_get_node_color(health_metrics)` → str | None
Determines node fill color based on health data.

```python
if error_rate > 10 or drop_rate > 10:
    return "lightcoral"  # Critical
elif error_rate > 5 or drop_rate > 5:
    return "lightyellow"  # Warning
else:
    return None  # Use default
```

**Parameters:**
- `health_metrics` (dict): Health info from API

**Returns:**
- Color name or `None` to use default

### `_get_edge_attributes(eps_value, max_eps)` → dict
Calculates edge styling (thickness & color) based on throughput.

```python
# Returns: {"penwidth": "3.5", "color": "orange"}
```

**Algorithm:**
1. Normalize EPS: `normalized = eps_value / max_eps`
2. Scale penwidth: `1 + (normalized * 4)` → range [1, 5]
3. Color buckets:
   - > 0.8 → darkred
   - 0.5-0.8 → orange
   - 0.2-0.5 → gold
   - < 0.2 → gray

## Usage Example

### Basic Graph with Metrics
```python
from cribl_api import get_cached_api_client
from graph_generator import generate_graph

# Get API client and generate graph
api_client = get_cached_api_client()
dot = generate_graph(api_client)

# Render as SVG
svg = dot.pipe(format="svg").decode("utf-8")
```

### Output Features
The generated graph will show:
- ✅ **Nodes** with color indicating health status
- ✅ **Edges** with thickness & color indicating throughput
- ✅ **Labels** with real-time EPS metrics
- ✅ **Descriptions** for each component

## Testing

### Test Coverage
- ✅ 10 new unit tests added
- ✅ Tests for helper functions (`_get_node_color`, `_get_edge_attributes`)
- ✅ Integration tests with mocked API responses
- ✅ Graceful failure scenarios

### Running Tests
```bash
python -m pytest tests/test_graph_generator.py -v
python -m pytest tests/test_cribl_api.py -v
```

### Key Test Cases
1. `test_generate_graph_with_health_status()` - Verifies color-coding
2. `test_generate_graph_with_edge_metrics()` - Verifies edge EPS display
3. `test_get_edge_attributes_*()` - Tests edge styling algorithm
4. `test_get_node_color_*()` - Tests health-to-color mapping

## Configuration & Environment Variables

No new environment variables required. Uses existing:
- `CRIBL_BASE_URL` - Cribl API endpoint
- `CRIBL_AUTH_TOKEN` or `CRIBL_USERNAME`/`CRIBL_PASSWORD` - Authentication

## Limitations & Future Work

### Current Limitations
1. **API Endpoint Availability** - Health and pipeline status endpoints may vary by Cribl version
2. **No Byte Throughput** - Only EPS metrics currently displayed (awaiting API support)
3. **No Historical Metrics** - Shows current state only (no time-series data)

### Future Enhancements
1. **Byte Rate Overlay** - Display MB/s or GB/s on edges
2. **Queue Depth Display** - Show queue sizes on nodes
3. **Latency Metrics** - Display pipeline processing latency
4. **Metric Aggregation** - Show total vs. per-pipeline throughput
5. **Custom Thresholds** - Configurable health warning/critical levels
6. **Metric History** - Trend analysis with color intensity
7. **Interactive Hover** - Detailed metrics in interactive mode
8. **Metric Export** - Include metrics in exported diagrams

## Architecture Notes

### Data Flow
```
CriblAPI
├── get_worker_groups()
├── get_sources() + get_source_status() + get_source_health()
├── get_destinations() + get_destination_status() + get_destination_health()
└── get_pipeline_status()
         ↓
   [Metrics Aggregation]
         ↓
   graph_generator.py
   ├── _get_node_color() [health → color]
   ├── _get_edge_attributes() [eps → styling]
   └── generate_graph() [creates visualization]
         ↓
   Graphviz Digraph with metrics overlaid
```

### Performance Considerations
- API calls are made in parallel (via threads) in Flask route
- Cached API client reduces authentication overhead
- Metric calculation is O(n) where n = number of components
- Graceful degradation if metrics unavailable

## Related Features

**See Also:**
- Feature #2: Configuration Analysis and Validation
- Feature #3: Interactive and Navigation Features
- Feature #4: Versioning and Environment Comparisons
- Feature #5: Documentation and Export

## References

- **API Documentation**: `docs/cribl_api_intro.md`
- **Code Reference**: `docs/CODE_REFERENCE.md`
- **Test Cases**: `tests/test_graph_generator.py`, `tests/test_cribl_api.py`

---

**Last Updated:** February 27, 2026  
**Implementation Level:** 75% Complete  
**Status:** Active Development
