# MAO Analytics Accessibility & Cross-Instance Collection

## 🎯 **THE PROBLEM**

**Current State**: MAO users can't easily review their analytics; data is scattered across local instances with no unified view or cross-instance aggregation.

**Solution**: Build **intelligent analytics dashboard** with **cross-instance data collection** that makes MAO's performance **transparent and actionable**.

---

## 🏗️ **CORE ANALYTICS INFRASTRUCTURE**

### 1.1 Unified Analytics Manager

```python
# CREATE: orchestrator/analytics_accessibility_manager.py

import json
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import pandas as pd
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class AnalyticsSnapshot:
    """Standardized analytics data structure"""
    timestamp: datetime
    instance_id: str
    user_id: str
    metrics: Dict[str, Any]
    performance_data: Dict[str, float]
    usage_patterns: Dict[str, int]
    error_logs: List[Dict[str, Any]]
    cost_estimates: Dict[str, float]

class AnalyticsAccessibilityManager:
    """Makes MAO analytics easily reviewable and actionable"""
    
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.analytics_path = config_path / "analytics"
        self.dashboard_path = config_path / "dashboard"
        self.ensure_analytics_structure()
    
    def ensure_analytics_structure(self):
        """Create analytics directory structure"""
        directories = [
            self.analytics_path / "user",
            self.analytics_path / "system", 
            self.analytics_path / "cross_instance",
            self.dashboard_path / "reports",
            self.dashboard_path / "visualizations"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    async def generate_user_analytics_report(self, user_id: str) -> Dict[str, Any]:
        """Generate comprehensive user analytics report"""
        
        # Collect all user analytics data
        user_data = await self._collect_user_data(user_id)
        
        # Generate insights and recommendations
        insights = await self._analyze_user_patterns(user_data)
        
        # Create actionable recommendations
        recommendations = await self._generate_recommendations(user_data, insights)
        
        # Build comprehensive report
        report = {
            "user_id": user_id,
            "generated_at": datetime.now().isoformat(),
            "period": "last_30_days",
            "summary": {
                "total_workflows_run": user_data.get("workflow_count", 0),
                "total_tokens_used": user_data.get("token_usage", 0),
                "estimated_cost": user_data.get("estimated_cost", 0),
                "success_rate": user_data.get("success_rate", 0),
                "most_used_tools": user_data.get("top_tools", []),
                "performance_score": user_data.get("performance_score", 0)
            },
            "detailed_metrics": user_data,
            "insights": insights,
            "recommendations": recommendations,
            "trends": await self._calculate_trends(user_data),
            "comparison": await self._compare_to_baseline(user_data)
        }
        
        # Save report for easy access
        await self._save_analytics_report(user_id, report)
        
        return report
    
    async def _collect_user_data(self, user_id: str) -> Dict[str, Any]:
        """Collect all analytics data for a user"""
        
        user_analytics_path = self.analytics_path / "user" / user_id
        
        if not user_analytics_path.exists():
            return {}
        
        # Collect workflow analytics
        workflow_data = await self._parse_workflow_analytics(user_analytics_path)
        
        # Collect tool usage analytics
        tool_data = await self._parse_tool_analytics(user_analytics_path)
        
        # Collect performance metrics
        performance_data = await self._parse_performance_analytics(user_analytics_path)
        
        # Collect cost estimates
        cost_data = await self._parse_cost_analytics(user_analytics_path)
        
        return {
            "workflows": workflow_data,
            "tools": tool_data,
            "performance": performance_data,
            "costs": cost_data,
            "errors": await self._parse_error_logs(user_analytics_path)
        }
    
    async def _analyze_user_patterns(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user patterns and generate insights"""
        
        insights = {
            "productivity_patterns": {},
            "cost_optimization": {},
            "performance_issues": [],
            "recommendations": []
        }
        
        # Analyze workflow patterns
        if user_data.get("workflows"):
            workflow_insights = await self._analyze_workflow_patterns(user_data["workflows"])
            insights["productivity_patterns"]["workflows"] = workflow_insights
        
        # Analyze tool usage patterns
        if user_data.get("tools"):
            tool_insights = await self._analyze_tool_patterns(user_data["tools"])
            insights["productivity_patterns"]["tools"] = tool_insights
        
        # Analyze cost patterns
        if user_data.get("costs"):
            cost_insights = await self._analyze_cost_patterns(user_data["costs"])
            insights["cost_optimization"] = cost_insights
        
        # Identify performance issues
        if user_data.get("performance"):
            performance_issues = await self._identify_performance_issues(user_data["performance"])
            insights["performance_issues"] = performance_issues
        
        return insights
    
    async def _generate_recommendations(self, user_data: Dict[str, Any], insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate actionable recommendations based on analytics"""
        
        recommendations = []
        
        # Cost optimization recommendations
        if insights.get("cost_optimization"):
            cost_recs = await self._generate_cost_recommendations(insights["cost_optimization"])
            recommendations.extend(cost_recs)
        
        # Performance improvement recommendations
        if insights.get("performance_issues"):
            perf_recs = await self._generate_performance_recommendations(insights["performance_issues"])
            recommendations.extend(perf_recs)
        
        # Workflow optimization recommendations
        if insights.get("productivity_patterns", {}).get("workflows"):
            workflow_recs = await self._generate_workflow_recommendations(insights["productivity_patterns"]["workflows"])
            recommendations.extend(workflow_recs)
        
        # Tool usage recommendations
        if insights.get("productivity_patterns", {}).get("tools"):
            tool_recs = await self._generate_tool_recommendations(insights["productivity_patterns"]["tools"])
            recommendations.extend(tool_recs)
        
        return recommendations
```

### 1.2 Cross-Instance Data Collection

```python
# CREATE: orchestrator/cross_instance_aggregator.py

import asyncio
import aiohttp
import json
from typing import Dict, List, Optional
from pathlib import Path
import hashlib
from datetime import datetime, timedelta

class CrossInstanceAggregator:
    """Collects and aggregates analytics from multiple MAO instances"""
    
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.aggregation_path = config_path / "analytics" / "cross_instance"
        self.aggregation_path.mkdir(parents=True, exist_ok=True)
        
        # Privacy settings
        self.anonymize_data = True
        self.aggregation_frequency = "daily"  # daily, weekly, monthly
        self.data_retention_days = 90
    
    async def collect_from_all_instances(self) -> Dict[str, Any]:
        """Collect analytics data from all known MAO instances"""
        
        # Get list of all MAO instances
        instances = await self._discover_instances()
        
        # Collect data from each instance
        instance_data = []
        for instance in instances:
            try:
                data = await self._collect_from_instance(instance)
                if data:
                    instance_data.append(data)
            except Exception as e:
                print(f"Failed to collect from instance {instance['id']}: {e}")
        
        # Aggregate the data
        aggregated_data = await self._aggregate_instance_data(instance_data)
        
        # Save aggregated data
        await self._save_aggregated_data(aggregated_data)
        
        return aggregated_data
    
    async def _discover_instances(self) -> List[Dict[str, Any]]:
        """Discover all MAO instances that should be aggregated"""
        
        instances = []
        
        # Check for local instance registry
        registry_path = self.config_path / "instance_registry.json"
        if registry_path.exists():
            with open(registry_path, 'r') as f:
                registry = json.load(f)
                instances.extend(registry.get("instances", []))
        
        # Check for network discovery (if enabled)
        if self._is_network_discovery_enabled():
            network_instances = await self._discover_network_instances()
            instances.extend(network_instances)
        
        return instances
    
    async def _collect_from_instance(self, instance: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Collect analytics data from a specific MAO instance"""
        
        instance_id = instance["id"]
        instance_path = Path(instance["path"])
        
        # Check if instance is accessible
        if not instance_path.exists():
            return None
        
        # Collect analytics data
        analytics_data = {
            "instance_id": instance_id,
            "collected_at": datetime.now().isoformat(),
            "instance_info": {
                "version": await self._get_instance_version(instance_path),
                "last_active": await self._get_last_active(instance_path),
                "user_count": await self._get_user_count(instance_path)
            },
            "aggregated_metrics": await self._collect_instance_metrics(instance_path),
            "performance_data": await self._collect_performance_data(instance_path),
            "usage_patterns": await self._collect_usage_patterns(instance_path)
        }
        
        # Anonymize data if enabled
        if self.anonymize_data:
            analytics_data = await self._anonymize_data(analytics_data)
        
        return analytics_data
    
    async def _aggregate_instance_data(self, instance_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate data from multiple instances"""
        
        if not instance_data:
            return {}
        
        # Aggregate basic metrics
        total_instances = len(instance_data)
        total_users = sum(inst["instance_info"]["user_count"] for inst in instance_data)
        
        # Aggregate performance metrics
        performance_metrics = await self._aggregate_performance_metrics(instance_data)
        
        # Aggregate usage patterns
        usage_patterns = await self._aggregate_usage_patterns(instance_data)
        
        # Calculate system-wide insights
        system_insights = await self._calculate_system_insights(instance_data)
        
        return {
            "aggregation_period": {
                "start": min(inst["collected_at"] for inst in instance_data),
                "end": max(inst["collected_at"] for inst in instance_data)
            },
            "instance_summary": {
                "total_instances": total_instances,
                "total_users": total_users,
                "average_users_per_instance": total_users / total_instances if total_instances > 0 else 0
            },
            "performance_metrics": performance_metrics,
            "usage_patterns": usage_patterns,
            "system_insights": system_insights,
            "anomalies": await self._detect_anomalies(instance_data)
        }
    
    async def _aggregate_performance_metrics(self, instance_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate performance metrics across instances"""
        
        all_metrics = []
        for instance in instance_data:
            if "performance_data" in instance:
                all_metrics.extend(instance["performance_data"])
        
        if not all_metrics:
            return {}
        
        # Calculate aggregate statistics
        df = pd.DataFrame(all_metrics)
        
        return {
            "average_response_time": df["response_time"].mean() if "response_time" in df.columns else 0,
            "average_success_rate": df["success_rate"].mean() if "success_rate" in df.columns else 0,
            "total_requests": len(df),
            "performance_distribution": {
                "fast": len(df[df["response_time"] < 1]) if "response_time" in df.columns else 0,
                "medium": len(df[(df["response_time"] >= 1) & (df["response_time"] < 5)]) if "response_time" in df.columns else 0,
                "slow": len(df[df["response_time"] >= 5]) if "response_time" in df.columns else 0
            }
        }
    
    async def _aggregate_usage_patterns(self, instance_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate usage patterns across instances"""
        
        all_patterns = defaultdict(int)
        
        for instance in instance_data:
            if "usage_patterns" in instance:
                for pattern, count in instance["usage_patterns"].items():
                    all_patterns[pattern] += count
        
        return dict(all_patterns)
    
    async def _calculate_system_insights(self, instance_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate system-wide insights from aggregated data"""
        
        insights = {
            "popular_features": [],
            "performance_trends": {},
            "usage_trends": {},
            "recommendations": []
        }
        
        # Identify popular features across all instances
        feature_usage = defaultdict(int)
        for instance in instance_data:
            if "usage_patterns" in instance:
                for feature, count in instance["usage_patterns"].items():
                    feature_usage[feature] += count
        
        insights["popular_features"] = sorted(
            feature_usage.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10]
        
        # Generate system-wide recommendations
        insights["recommendations"] = await self._generate_system_recommendations(instance_data)
        
        return insights
```

### 1.3 Analytics Dashboard Interface

```python
# CREATE: interfaces/analytics_dashboard.py

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import json
from pathlib import Path

class AnalyticsDashboard:
    """Interactive analytics dashboard for MAO users"""
    
    def __init__(self, analytics_manager, config_path: Path):
        self.analytics_manager = analytics_manager
        self.config_path = config_path
    
    def render_dashboard(self):
        """Render the main analytics dashboard"""
        
        st.set_page_config(
            page_title="MAO Analytics Dashboard",
            page_icon="📊",
            layout="wide"
        )
        
        st.title("📊 MAO Analytics Dashboard")
        
        # Sidebar for navigation
        page = st.sidebar.selectbox(
            "Dashboard Sections",
            ["Overview", "Performance", "Usage Patterns", "Cost Analysis", "Recommendations", "Cross-Instance"]
        )
        
        if page == "Overview":
            self._render_overview_page()
        elif page == "Performance":
            self._render_performance_page()
        elif page == "Usage Patterns":
            self._render_usage_patterns_page()
        elif page == "Cost Analysis":
            self._render_cost_analysis_page()
        elif page == "Recommendations":
            self._render_recommendations_page()
        elif page == "Cross-Instance":
            self._render_cross_instance_page()
    
    def _render_overview_page(self):
        """Render the overview page with key metrics"""
        
        st.header("📈 Overview")
        
        # Get user analytics report
        user_id = st.session_state.get("user_id", "default")
        report = asyncio.run(self.analytics_manager.generate_user_analytics_report(user_id))
        
        if not report:
            st.warning("No analytics data available. Start using MAO to see your metrics!")
            return
        
        # Key metrics cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Workflows",
                value=report["summary"]["total_workflows_run"],
                delta=report.get("trends", {}).get("workflow_growth", 0)
            )
        
        with col2:
            st.metric(
                label="Success Rate",
                value=f"{report['summary']['success_rate']:.1f}%",
                delta=report.get("trends", {}).get("success_rate_change", 0)
            )
        
        with col3:
            st.metric(
                label="Tokens Used",
                value=f"{report['summary']['total_tokens_used']:,}",
                delta=report.get("trends", {}).get("token_growth", 0)
            )
        
        with col4:
            st.metric(
                label="Estimated Cost",
                value=f"${report['summary']['estimated_cost']:.2f}",
                delta=report.get("trends", {}).get("cost_change", 0)
            )
        
        # Performance score
        st.subheader("🎯 Performance Score")
        performance_score = report["summary"]["performance_score"]
        
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=performance_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Overall Performance"},
            delta={'reference': 80},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"},
                    {'range': [80, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Top tools usage
        st.subheader("🔧 Most Used Tools")
        top_tools = report["summary"]["most_used_tools"]
        
        if top_tools:
            tool_data = pd.DataFrame(top_tools)
            fig = px.bar(
                tool_data, 
                x="usage_count", 
                y="tool_name",
                orientation="h",
                title="Tool Usage Frequency"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def _render_performance_page(self):
        """Render detailed performance analytics"""
        
        st.header("⚡ Performance Analytics")
        
        # Get performance data
        user_id = st.session_state.get("user_id", "default")
        report = asyncio.run(self.analytics_manager.generate_user_analytics_report(user_id))
        
        if not report or "detailed_metrics" not in report:
            st.warning("No performance data available.")
            return
        
        performance_data = report["detailed_metrics"].get("performance", {})
        
        # Response time trends
        if "response_times" in performance_data:
            st.subheader("📊 Response Time Trends")
            
            df = pd.DataFrame(performance_data["response_times"])
            fig = px.line(
                df, 
                x="timestamp", 
                y="response_time",
                title="Response Time Over Time"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Success rate analysis
        if "success_rates" in performance_data:
            st.subheader("✅ Success Rate Analysis")
            
            df = pd.DataFrame(performance_data["success_rates"])
            fig = px.line(
                df, 
                x="timestamp", 
                y="success_rate",
                title="Success Rate Over Time"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Error analysis
        if "errors" in report["detailed_metrics"]:
            st.subheader("🚨 Error Analysis")
            
            errors = report["detailed_metrics"]["errors"]
            if errors:
                error_df = pd.DataFrame(errors)
                error_counts = error_df["error_type"].value_counts()
                
                fig = px.pie(
                    values=error_counts.values,
                    names=error_counts.index,
                    title="Error Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
    
    def _render_cost_analysis_page(self):
        """Render cost analysis and optimization insights"""
        
        st.header("💰 Cost Analysis")
        
        user_id = st.session_state.get("user_id", "default")
        report = asyncio.run(self.analytics_manager.generate_user_analytics_report(user_id))
        
        if not report:
            st.warning("No cost data available.")
            return
        
        cost_data = report["detailed_metrics"].get("costs", {})
        
        # Cost breakdown
        if "cost_breakdown" in cost_data:
            st.subheader("📊 Cost Breakdown")
            
            cost_breakdown = cost_data["cost_breakdown"]
            fig = px.pie(
                values=list(cost_breakdown.values()),
                names=list(cost_breakdown.keys()),
                title="Cost Distribution by Component"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Cost optimization recommendations
        if "recommendations" in report:
            st.subheader("💡 Cost Optimization Recommendations")
            
            cost_recs = [rec for rec in report["recommendations"] if rec.get("category") == "cost"]
            
            for rec in cost_recs:
                with st.expander(f"💡 {rec['title']}"):
                    st.write(rec["description"])
                    if "potential_savings" in rec:
                        st.metric("Potential Savings", f"${rec['potential_savings']:.2f}")
    
    def _render_cross_instance_page(self):
        """Render cross-instance analytics"""
        
        st.header("🌐 Cross-Instance Analytics")
        
        # Get cross-instance data
        aggregator = CrossInstanceAggregator(self.config_path)
        aggregated_data = asyncio.run(aggregator.collect_from_all_instances())
        
        if not aggregated_data:
            st.warning("No cross-instance data available.")
            return
        
        # Instance summary
        st.subheader("📊 Instance Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Total Instances",
                aggregated_data["instance_summary"]["total_instances"]
            )
        
        with col2:
            st.metric(
                "Total Users",
                aggregated_data["instance_summary"]["total_users"]
            )
        
        with col3:
            st.metric(
                "Avg Users/Instance",
                f"{aggregated_data['instance_summary']['average_users_per_instance']:.1f}"
            )
        
        # Popular features across instances
        if "usage_patterns" in aggregated_data:
            st.subheader("🔥 Popular Features Across Instances")
            
            usage_data = aggregated_data["usage_patterns"]
            if usage_data:
                df = pd.DataFrame(list(usage_data.items()), columns=["Feature", "Usage Count"])
                df = df.sort_values("Usage Count", ascending=False).head(10)
                
                fig = px.bar(
                    df, 
                    x="Usage Count", 
                    y="Feature",
                    orientation="h",
                    title="Most Popular Features"
                )
                st.plotly_chart(fig, use_container_width=True)
```

---

## 🚀 **IMPLEMENTATION ROADMAP**

### Week 1: Core Analytics Infrastructure
- [ ] Analytics accessibility manager
- [ ] Cross-instance data collection
- [ ] Basic dashboard interface
- [ ] Data anonymization and privacy controls

### Week 2: Dashboard & Visualization
- [ ] Interactive Streamlit dashboard
- [ ] Performance trend analysis
- [ ] Cost optimization insights
- [ ] Usage pattern visualization

### Week 3: Cross-Instance Aggregation
- [ ] Multi-instance data collection
- [ ] Privacy-compliant aggregation
- [ ] System-wide insights
- [ ] Anomaly detection

### Week 4: Advanced Analytics
- [ ] Predictive analytics
- [ ] Automated recommendations
- [ ] Performance benchmarking
- [ ] Cost forecasting

---

## 💎 **SUCCESS METRICS**

**User Experience:**
- **Analytics Accessibility**: 100% of users can access their analytics within 3 clicks
- **Dashboard Load Time**: <2 seconds for full dashboard
- **Insight Quality**: >90% of recommendations are actionable

**Cross-Instance Benefits:**
- **Data Coverage**: 95% of MAO instances contribute to aggregate analytics
- **Privacy Compliance**: 100% of data is properly anonymized
- **System Insights**: Identify top 10 most valuable features across all instances

**Performance Impact:**
- **Collection Overhead**: <1% performance impact during data collection
- **Storage Efficiency**: 90% reduction in analytics storage requirements
- **Real-time Updates**: <5 second delay for cross-instance data updates

---

## 🔥 **THE VISION**

Transform MAO from **black box** to **transparent, actionable insights**. Users can finally **see** what MAO is doing, **optimize** their usage, and **contribute** to system-wide improvements while maintaining complete privacy.

**This is how we make MAO truly reviewable and improvable!** 📊✨ 