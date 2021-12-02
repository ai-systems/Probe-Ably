import React from "react";
import fireparrot from "../../assets/fireparrot.gif"

const ProgressBar = ({ taskProgress, modelProgress, probesProgress }) => {

  const containerStyles = {
    height: 20,
    width: '400px',
    backgroundColor: "#e0e0de",
    borderRadius: 50,
    margin: 50
  }

  const taskFillerStyles = {
    height: '100%',
    width: `${(taskProgress.n * 100) / taskProgress.total}%`,
    backgroundColor: 'green',
    borderRadius: 'inherit',
    textAlign: 'right',
    transition: 'width 1s ease-in-out',
  }
  const modelFillerStyles = {
    height: '100%',
    width: `${(modelProgress.n * 100) / modelProgress.total}%`,
    backgroundColor: 'red',
    borderRadius: 'inherit',
    textAlign: 'right',
  }
  const probesFillerStyles = {
    height: '100%',
    width: `${(probesProgress.n * 100) / probesProgress.total}%`,
    backgroundColor: 'red',
    borderRadius: 'inherit',
    textAlign: 'right',
  }

  const labelStyles = {
    color: 'white',
    fontWeight: 'bold',
    height: '90%',
    paddingRight: '3px',
  }
  const imgStyle = {
    paddingRight: '3px',
    height: '90%',
  }

  return (
  <>
     <div>"Tasks:"</div>
    <div style={containerStyles}>
      <div style={taskFillerStyles}>
        <span style={labelStyles}>{`${taskProgress.n}/${taskProgress.total}`}</span>
      </div>
    </div>
	  <div>"Representations:"</div>
    <div style={containerStyles}>
      <div style={modelFillerStyles}>
        <span style={labelStyles}>{`${modelProgress.n}/${modelProgress.total}`}</span>
      </div>
    </div>
	  <div>"Training Probes:"</div>	
    <div style={containerStyles}>
      <div style={probesFillerStyles}>
        <span style={labelStyles}>{`${probesProgress.n}/${probesProgress.total}`}<img style={imgStyle} src={fireparrot}/></span>
      </div>
    </div>
  </>
  )};

export default ProgressBar;
