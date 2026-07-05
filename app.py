import streamlit as st
import os
import sys
import json
import pandas as pd
from pathlib import Path
sys.path.append(os.path.abspath("src")) # type: ignore

from matchmind.pipeline.runner import PipelineRunner # type: ignore

# Setup Page
st.set_page_config(page_title="MatchMind Dashboard", layout="wide", page_icon="⚽")

st.title("⚽ MatchMind: Tactical Intelligence Dashboard")
st.markdown("Analyze professional football footage with state-of-the-art Computer Vision & Geometric Intelligence.")

# Sidebar
st.sidebar.header("Control Panel")
uploaded_file = st.sidebar.file_uploader("Upload Match Video", type=["mp4", "avi"])

if st.sidebar.button("Run Analysis", type="primary"):
    if uploaded_file is not None:
        with st.spinner("Initializing CV Pipeline and Tactical Engines..."):
            os.makedirs("data/temp", exist_ok=True)
            temp_path = os.path.join("data/temp", uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
                
            runner = PipelineRunner(config=None)
            out_video, minimap_video = runner.run(temp_path)
            
            if out_video and minimap_video:
                st.session_state['out_video'] = out_video
                st.session_state['minimap_video'] = minimap_video
                st.sidebar.success("Analysis Complete!")
            else:
                st.sidebar.error("Analysis Failed!")
    else:
        st.sidebar.warning("Please upload a video first!")
        
st.sidebar.markdown("---")
if st.sidebar.button("Train Custom YOLO Model", type="secondary"):
    with st.spinner("Training Model... (This will take a while)"):
        import subprocess
        result = subprocess.run(["python", "main.py", "--train"], capture_output=True, text=True)
        if result.returncode == 0:
            st.sidebar.success("Training Complete! Weights saved to outputs/weights/custom_yolo11.pt")
        else:
            st.sidebar.error("Training Failed! Check console logs.")
            st.sidebar.text(result.stderr)

# Load Mocked Data
out_dir = Path("outputs/dashboard")
data_loaded = out_dir.exists()

# Main Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📹 Match Vision", 
    "📈 Possession & Build-up", 
    "🛡️ Team Compactness", 
    "🔥 Player Profiler", 
    "⚡ Transitions",
    "🧠 Predictive Intelligence"
])

with tab1:
    st.header("Computer Vision Feed")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Raw Feed (YOLO11 + ByteTrack)")
        if 'out_video' in st.session_state and os.path.exists(st.session_state['out_video']):
            st.video(st.session_state['out_video'])
        else:
            st.info("Upload a video and run analysis to view the Computer Vision feed.")
    with col2:
        st.subheader("Live 2D Bird's-Eye Minimap")
        if 'minimap_video' in st.session_state and os.path.exists(st.session_state['minimap_video']):
            st.video(st.session_state['minimap_video'])
        else:
            st.info("Run analysis to generate the 2D Pitch Map.")

with tab2:
    st.header("Possession Timeline")
    st.progress(60, text="Possession: Team A (60%) vs Team B (40%)")
    
    st.subheader("Attack Build-ups Detected")
    if data_loaded and (out_dir / "buildups.json").exists():
        with open(out_dir / "buildups.json") as f:
            buildups = json.load(f)
            
        if buildups:
            for i, b in enumerate(buildups):
                with st.expander(f"⚡ Build-up Sequence {i+1} (Team {b['team']})", expanded=True):
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Duration (Frames)", b['duration'])
                    c2.metric("Players Involved", len(b['players']))
                    c3.metric("Started In", b['start_zone'])
                    
                    if b['forward_progression']:
                        c4.metric("Outcome", "Progressed Forward 🚀")
                    else:
                        c4.metric("Outcome", "Stalled 🛑")
        else:
            st.info("No substantial build-ups detected in this clip.")
            
    st.markdown("---")
    st.subheader("Match Understanding: Ball Control Timeline")
    if data_loaded and (out_dir / "possession_states.json").exists():
        with open(out_dir / "possession_states.json") as f:
            states = json.load(f)
        if states:
            # Draw a timeline of states
            for s in states:
                if s['control_changed']:
                    st.warning(f"🔄 **TURNOVER** at Frame {s['frame']}! Team {s['team']} is now **{s['state']}** the ball.")
                elif s['state'] == "Contesting":
                    st.error(f"⚔️ **CONTESTED** at Frame {s['frame']}! Multiple players around the ball.")
        else:
            st.info("No state changes detected.")
    else:
        st.warning("Please run analysis first.")

with tab3:
    st.subheader("Convex Hull & Compactness")
    if data_loaded and (out_dir / "compactness.json").exists():
        with open(out_dir / "compactness.json") as f:
            comp_data = json.load(f)
            df = pd.DataFrame(comp_data)
            if not df.empty and "frame" in df.columns:
                st.line_chart(df, x="frame", y=["width", "depth", "area"], color=["#FF0000", "#0000FF", "#00FF00"])
            else:
                st.info("Not enough players detected to form compactness hulls.")
    else:
        st.warning("Please run analysis first.")

with tab4:
    st.subheader("Positional Role Estimation")
    if data_loaded and (out_dir / "positional.json").exists():
        with open(out_dir / "positional.json") as f:
            pos_data = json.load(f)
            
        if pos_data:
            player_id = st.selectbox("Select Player", list(pos_data.keys()))
            if player_id:
                st.metric(label="Estimated Tactical Role", value=pos_data[player_id]["role"])
                st.metric(label="Average Location (X, Y)", value=f"{pos_data[player_id]['avg_x']:.2f}, {pos_data[player_id]['avg_y']:.2f}")
        else:
            st.info("No positional data extracted.")
    else:
        st.warning("Please run analysis first.")

with tab5:
    st.subheader("Counterattack Transitions")
    if data_loaded and (out_dir / "counterattacks.json").exists():
        with open(out_dir / "counterattacks.json") as f:
            st.json(json.load(f))
    else:
        st.warning("Please run analysis first.")

with tab6:
    st.header("Predictive Intelligence")
    st.markdown("Dynamic probabilistic forecasting generated via Geometric Heuristics.")
    
    if data_loaded and (out_dir / "predictive.json").exists():
        with open(out_dir / "predictive.json") as f:
            predictive_data = json.load(f)
            
        if predictive_data:
            latest = predictive_data[-1]
            st.subheader(f"Latest Inference (Frame {latest['frame']})")
            
            c1, c2, c3 = st.columns(3)
            
            # Pass Success
            c1.metric(
                "Pass Success Likelihood", 
                f"{latest['pass_success']:.1f}%",
                delta="Optimal" if latest['pass_success'] > 60 else "Risky",
                delta_color="normal" if latest['pass_success'] > 60 else "inverse"
            )
            
            # Loss Risk
            c2.metric(
                "Possession Loss Risk", 
                f"{latest['loss_risk']:.1f}%",
                delta="Critical" if latest['loss_risk'] > 70 else "Safe",
                delta_color="inverse"
            )
            
            # Dangerous Phase
            c3.metric(
                "Dangerous Phase Probability", 
                f"{latest['danger_prob']:.1f}%",
                delta="High Threat" if latest['danger_prob'] > 50 else "Low Threat",
                delta_color="normal" if latest['danger_prob'] > 50 else "off"
            )
            
            st.markdown("---")
            st.subheader("Raw Probabilistic Timeline")
            st.json(predictive_data)
        else:
            st.info("Not enough data to run predictive models.")
    else:
        st.warning("Please run analysis first.")
