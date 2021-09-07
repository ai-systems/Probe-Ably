import React, { useEffect } from "react";
import ProgressBar from "./ProgressBar"

const Report = ({ taskProgress, modelProgress, probesProgress, setTaskProgress, setModelProgress, setProbesProgress }) => {

    useEffect(() => {
      const interval = setInterval(() => {
        fetch("/task_progress")
        .then((res) => res.json())
        .then(progress => {setTaskProgress(progress)})
      }, 500);

      return () => clearInterval(interval);
    }, [taskProgress, setTaskProgress]);

    useEffect(() => {
      const interval = setInterval(() => {
        fetch("/model_progress")
        .then((res) => res.json())
        .then((prog)=>{setModelProgress(prog)});
      }, 500);
      return () => clearInterval(interval);
    }, [modelProgress, setModelProgress]);

    useEffect(() => {
      const interval = setInterval(() => {
        fetch("/probes_progress")
        .then((res) => res.json())
        .then((prog)=>{setProbesProgress(prog)});
      }, 500);
      return () => clearInterval(interval);
    }, [probesProgress, setProbesProgress]);


    return (
    <ProgressBar taskProgress={taskProgress} modelProgress={modelProgress} probesProgress={probesProgress}/>
    )
    }

export default Report
