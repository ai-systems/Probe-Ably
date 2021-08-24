import React, { useEffect, useState } from "react";
import ProgressBar from "./ProgressBar"

const Report = () => {

	const [taskProgress, setTaskProgress] = useState(0)
	const [modelProgress, setModelProgress] = useState(0)
	const [probesProgress, setProbesProgress] = useState(0)

	useEffect(() => {
	  const interval = setInterval(() => {
	    fetch("/task_progress")
		  .then((prog_data)=> prog_data.json())
		  .then((prog)=>{setTaskProgress(prog)});
	  }, 500);

	  return () => clearInterval(interval);
	}, []);

	useEffect(() => {
	  const interval = setInterval(() => {
	    fetch("/model_progress")
		  .then((prog_data)=> prog_data.json())
		  .then((prog)=>{setModelProgress(prog)});
	  }, 500);
	  return () => clearInterval(interval);
	}, []);

	useEffect(() => {
	  const interval = setInterval(() => {
	    fetch("/probes_progress")
		  .then((prog_data)=> prog_data.json())
		  .then((prog)=>{setProbesProgress(prog)});
	  }, 500);
	  return () => clearInterval(interval);
	}, []);


	return (
	<ProgressBar taskProgress={taskProgress} modelProgress={modelProgress} probesProgress={probesProgress}/>
	)
	}

export default Report
