  import { useState, useEffect, useCallback } from "react";
  import "./App.css";
  import CalculatorModal from "./CalculatorInput";
  import { waveFunctionCollapseDesc, rotatingParticle, InformatioLoss, PreparedQuantumState, SpinOneSystem } from "./demoCases";
  import Instructions from "./Instructions";

  type Axis = "x" | "y" | "z" | "θ/φ";
  type StateType = "R" | "ψ";
  type SpinType = "1/2" | "1";


  // key interfaces, when each one is called they must have this information
  interface Analyser {
    axis: Axis;
    upSelected: boolean;
    downSelected: boolean;
    // only needed if in spin-1 or if using theta/phi axis
    zeroSelected?: boolean; 
    theta?: string;   // stored as raw string so user can type e.g. "π/2"
    phi?: string;
  }

  interface ResultCount {
    up: number;
    down: number;
    zero?: number;
  }

  interface Coeffs {
    a: string;
    b: string;
    c?: string;
  }


  // when defining the experiements we need these paramters
  interface DemoCase {
    label: string;
    description: 
    {
      title: string;
      setup: string[];
      observe: string[];
      explanation: string;
    };
    spinType: SpinType;
    numAnalysers: number;
    analysers: Analyser[];
    atoms: number;
    stateType: StateType;
    coeffs?: Coeffs;  
  }


  // list of speed options in the drop down
  const Particle_flow_speed = [
    {label: "Slow", value: 1000},
    {label: "Normal", value: 500},
    {label: "Fast", value: 250},
    {label: "Very Fast", value: 100},
    {label: "Ultra", value: 50},];

  // look up table, when we are given a speed value return the label
  const Speed_label: Record<number, string> = {
    1000: "Slow",
    500:  "Normal",
    250:  "Fast",
    100:  "Very Fast",
    50:   "Ultra",
  };

  //avalable axis options
  const AXES: Axis[] = ["x", "y", "z", "θ/φ"];


  //converting radians into degrees
  //function takes in either a string or nothing (nothing when were not using theta/phi)
  function AngleToDegrees(val: string | undefined): number {

    if (!val) return 0; //return 0 if no value given

    const cleanInput = val.trim();

    if (!cleanInput) return 0; //if the string is empty after trimming return 0

    if (cleanInput.includes("π")) 
      {
      const replacePi = cleanInput.replace(/π/g, `(${Math.PI})`);// replace π with its numeric value and evaluate the expression as radians
      try 
      {
        // eslint-disable-next-line no-new-func
        const radians = new Function(`"use strict"; return (${replacePi})`)() as number;
        return radians * (180 / Math.PI);

      } 
      catch 
      {
        return 0;
      }
    }

    return parseFloat(cleanInput) || 0; //if no pi, just degrees
  }


  // function to check what paths are open for particles 
  function buildPath(an: Analyser, spinType: SpinType)
  {

    if (spinType === "1/2") 
    {
      if (an.upSelected && an.downSelected) return "all";
      if (an.upSelected) return "up";
      if (an.downSelected) return "down";
      return "none";
    } 
    
    else if (spinType === "1") 
    {
      if (an.upSelected && an.zeroSelected && an.downSelected) return "all";
      if (an.upSelected && an.zeroSelected) return "up,zero";
      if (an.upSelected && an.downSelected) return "up,down";
      if (an.zeroSelected && an.downSelected) return "zero,down";
      if (an.upSelected) return "up";
      if (an.zeroSelected) return "zero";
      if (an.downSelected) return "down";
      return "none";
    }

  }

  //what the analysers default to when created
  function makeAnalyser(spinType: SpinType): Analyser {
    
    if (spinType === "1/2") {
      return {
        axis: "z",
        upSelected: true,
        downSelected: true,
        theta: "0",
        phi: "0",
      };
    }

    else {
      return {
        axis: "z",
        upSelected: true,
        downSelected: true,
        zeroSelected: true,
        theta: "0",
        phi: "0",
      };
    }

  }

  // Main UI component

  function SternGerlachSim() {
    // initial state for all components when user opens the site

    // simualtion config
    const [spinType, setSpinType] = useState<SpinType>("1/2");
    const [numAnalysers, setNumAnalysers] = useState(1);
    const [analysers, setAnalysers] = useState<Analyser[]>([makeAnalyser("1/2")]);
    const [atoms, setAtoms] = useState(10000);

    // state config
    const [stateType, setStateType] = useState<StateType>("R");
    const [coeffs, setCoeffs] = useState<Coeffs>({ a: "", b: "", c: "" });
    const [normWarning, setNormWarning] = useState(false);

    // result config
    const [result, setResult] = useState<ResultCount | null>(null);
    const [loading, setLoading] = useState(false);

    // stream config
    const [streaming, setStreaming] = useState(false);
    const [streamSpeed, setStreamSpeed] = useState(500);

    // UI config
    const [showCalculator, setShowCalculator] = useState(false);
    const [openAxisDropdown, setOpenAxisDropdown] = useState<number | null>(null);
    const [openSpeedDropdown, setOpenSpeedDropdown] = useState(false);
    const [activeDemo, setActiveDemo] = useState<DemoCase | null>(null);
    const [bottomOpen, setBottomOpen] = useState(false);
    const [particlesFired, setParticlesFired] = useState(0);

    // each time a user changes spinType or numAnalysers we need to rebuild the analysers array
    useEffect(() => {

      if (activeDemo !== null) return; // if we are applying a demo case, skip the rebuild otherwise defaul overides our custum case

      // build new array of default analysers 
      const newAnalysers = [];
      for (let i = 0; i < numAnalysers; ++i)
      {
        newAnalysers.push(makeAnalyser(spinType));
      }
      setAnalysers(newAnalysers);
    }, [numAnalysers, spinType, activeDemo]); // only re runs when one of these types change

    // closing drops downs
    useEffect(() => {

      if (openAxisDropdown === null && !openSpeedDropdown) return;

      function openAxisDropdown(clickedSpot: HTMLElement)
      {
        const clickedOnDropdown = clickedSpot.closest(".axis-selector-wrapper");
        if (!clickedOnDropdown)
        {
          setOpenAxisDropdown(null);
        }
      }

      function openSpeedDropdown(clickedSpot: HTMLElement)
      {
        const clickedOnDropdown = clickedSpot.closest(".speed-selector-wrapper");
        if (!clickedOnDropdown)
        {
          setOpenSpeedDropdown(false);
        }
      }

      function clicking(click: MouseEvent)
      {
        const clickedSpot  = click.target as HTMLElement;
        openAxisDropdown(clickedSpot);
        openSpeedDropdown(clickedSpot);
      }

      document.addEventListener("mousedown", clicking);

      return () => {
        document.addEventListener("mousedown", clicking);
      }
    }, [openAxisDropdown, openSpeedDropdown]);

    // handling when an analysers paths are changed
    const changePathChoice = (index: number, choice: "up" | "down" | "zero") => {
    
      
      const newPathAnalysers = analysers.map((analyser, i) => {

        if (i !== index) 
        {
          return analyser;
        }

        // need a copy of original so when we hand back an updated version with changes, React knows something has changed and rebuilds the analysers 
        const updateAnalyser = {...analyser};

        // if the box was clicked flip its selection (if it was selected unselect and vice versa)
        if (choice === "up")
        {
          updateAnalyser.upSelected = !analyser.upSelected;
        }

        else if (choice === "down")
        {
          updateAnalyser.downSelected = !analyser.downSelected;
        }

        else if (choice === "zero")
        {
          updateAnalyser.zeroSelected = !analyser.zeroSelected;
        }

        return updateAnalyser;

      });

      //React sees new build and redraws
      setAnalysers(newPathAnalysers)
    };


    const updateAnalyserConfig = (index: number, patch: Partial<Analyser>) => {

      const updatedAnalysers = analysers.map((an, i) => {

        if (i !== index) 
        {
          return an;
        }

        const updatedAnalyser = { ...an, ...patch };

        return updatedAnalyser;

      });

      setAnalysers(updatedAnalysers);
    };

  // Appends "π" to whichever angle field the user clicked
    const appendPi = (index: number, angle: "theta" | "phi") => {

      const an = analysers[index]; //finds out which analyser user clicked on

      const currentValue = an[angle] ?? ""; //finds out current value in the box

      let newValue = "";

      // If the box is empty or "0", replace it with π
      if (currentValue === "" || currentValue === "0")
      {
        newValue = "π"
      }
      else //else add π to the end of the current value
      {
        newValue = currentValue + "π";
      }
      updateAnalyserConfig(index, { [angle]: newValue });
    };

  //Setup for the experiements I designed as examples. Each example requires the interface defined above.
    const demonstationCases: DemoCase[] = [
      {
        label: "Wave Function Collapse",
        description: waveFunctionCollapseDesc,
        spinType: "1/2",
        numAnalysers: 2,
        stateType: "R",
        atoms: 10000,
        analysers: [{axis: "z", upSelected: true, downSelected: false, theta: "0", phi: "0"},
                  {axis: "z", upSelected: true, downSelected: true, theta: "0", phi: "0"}],
      },

      {
        label: "180° Rotation",
        description: rotatingParticle,
        spinType: "1/2",
        numAnalysers: 2,
        stateType: "R",
        atoms: 10000,
        analysers: [{axis: "z", upSelected: true, downSelected: false, theta: "0", phi: "0"},
                  {axis: "θ/φ", upSelected: true, downSelected: true, theta: "180", phi: "0"}],    
      },

      {
        label: "Information loss",
        description: InformatioLoss,
        spinType: "1/2",
        numAnalysers: 3,
        stateType: "R",
        atoms: 10000,
        analysers: [{axis: "z", upSelected: true, downSelected: false, theta: "0", phi: "0"},
                  {axis: "x", upSelected: false, downSelected: true, theta: "0", phi: "0"},
                  {axis: "z", upSelected:true, downSelected:true, theta: "0", phi: "0"}],  
      },

      {
        label: "Prepared quantum state",
        description: PreparedQuantumState,
        spinType: "1/2",
        numAnalysers: 1,
        stateType: "ψ",
        atoms: 10000,
        coeffs: {a: "1/2", b: "((√(3)/2)*(e^(i*π/4)))" },
        analysers: [{axis: "z", upSelected: true, downSelected: true, theta: "0", phi: "0"},],
      },

      {
        label: "Spin One Measurement",
        description: SpinOneSystem,
        spinType: "1",
        numAnalysers: 2,
        stateType: "R",
        atoms: 10000,
        analysers: [{axis: "z", upSelected: true, zeroSelected:false, downSelected:false, theta: "0", phi: "0"},
                  {axis: "x", upSelected:true, zeroSelected:true, downSelected:true, theta: "0", phi: "0"}
        ],    
      }


    ];


    //when a user selects a demo this function applies the demo to the users screen
    const ApplyDemo = (demo: DemoCase) => {
      setSpinType(demo.spinType);
      setStateType(demo.stateType)
      setNumAnalysers(demo.numAnalysers);
      setAnalysers(demo.analysers);
      setAtoms(demo.atoms);
      setResult(null);
      setActiveDemo(demo)
      if (demo.coeffs) setCoeffs(demo.coeffs); 
    };

  //when user resets this is what everything resets to.
    const resetSimulator = () => {
      setSpinType("1/2");
      setNumAnalysers(1);
      setAnalysers([makeAnalyser("1/2")]);
      setAtoms(10000);
      setStateType("R");
      setCoeffs({ a: "", b: "", c: "" });
      setResult(null);
      setStreaming(false);
      setStreamSpeed(500);
      setActiveDemo(null);
      setNormWarning(false);
      setOpenAxisDropdown(null);
      setOpenSpeedDropdown(false);
      setBottomOpen(true);
      setParticlesFired(0);
    };

    //key function, builds the package of inputs and sends it to the backend
    //atomcount is the amount of atoms the user wants to fire, is streaming boolean indicates if user wants full bulk or a stream
    const buildPythonPackage = useCallback((atomCount: number, isStreaming: boolean) => {
      const analyserData = analysers.map(analyser => {
        return {
          axis: analyser.axis,
          filter: buildPath(analyser, spinType), //what poaths has the user allowed
          theta: AngleToDegrees(analyser.theta), // convert theta string to degrees
          phi: AngleToDegrees(analyser.phi), //convert phi string to degrees
        };
      });
      
      //only include coeeficents if the ψ mode is selected
      let a = undefined;
      if (stateType === "ψ")
      {
        a = coeffs.a
      }

      let b = undefined;
      if (stateType === "ψ")
      {
        b = coeffs.b
      }

      let c = undefined;
      if (stateType === "ψ" && spinType === "1") 
      {
      c = coeffs.c;
      }

      //build the data package for the backend
      const pythonPackage = {
        SQN: spinType,
        analysers: analyserData,
        atoms:atomCount,
        a: a,
        b: b,
        c: c,
        streaming: isStreaming,
      };

      return pythonPackage;
    }, [spinType, analysers, stateType, coeffs]);

    //function for running the measurement, async so we can allow the function to wait for backend to respond before moving on
    const runMeasurement = async () => {
      setLoading(true); //set loading to true so no measurement can be run anymore
      setResult(null); //resets result everytime
      try 
      {
        //send the measurement deatils to the backend
        const result  = await fetch(`${process.env.REACT_APP_API_URL}/measurements`, { //send POST request to teh backend with the measurement package
          method:  "POST",
          headers: { "Content-Type": "application/json" }, //lets the backend know the data is formatted as JSON
          body:    JSON.stringify(buildPythonPackage(atoms, false)), //convert the python package to a string
        });

        const data = await result.json(); //extract results
        
        //if backend has an error return all zeros, otherwise display results 
        if (data.error)
        {
          setResult({ up: 0, down: 0, zero: 0 });
          console.error(data.error);
        }
        else
        {
          setResult(data.results[0])
        }

        //function Paul wanted to check if the state needs normalising
        let normValue = false;
        if (data.need_to_norm !== undefined && data.need_to_norm !== null)
        {
          normValue = data.need_to_norm;
        }
        setNormWarning(normValue); //tell user if we needed to normalise
      }
        catch (err)
          {
          console.error(err);
          setResult({ up: 0, down: 0, zero: 0 });
          }
        
        //last step of any run measurement, turn off loading so user can make another run
        finally
        {
          setLoading(false)
        }
      };

    useEffect(() => {

      // if streaming is not active, do nothing
      if (!streaming) return;

      // this function runs once per interval tick — sends one atom at a time to the backend
      const tick = async () => {
        try
        {
          // same as runMeasurement but sends 1 atom and marks it as streaming
          const res = await fetch(`${process.env.REACT_APP_API_URL}/measurements`, {
          method:  "POST",
          headers: { "Content-Type": "application/json" },
          body:    JSON.stringify(buildPythonPackage(1, true)),
          
          });

          const data = await res.json();
          setParticlesFired(prev => prev + 1);
          setLoading(false);
          if (data.need_to_norm) {
          setNormWarning(true);
}

          if (!data.results) return;

          // add the new result to the running total
          // prev is whatever the current result is, we add the new counts on top
          setResult(prev => {

            // if there are no previous results yet, start from zero
            const p = prev ?? { up: 0, down: 0, zero: 0 };

            // only track zero count if we are in spin-1 mode
            let zero = undefined;
            if (spinType === "1")
            {
              let previousZero = 0;
              if (p.zero !== undefined && p.zero !== null)
              {
                previousZero = p.zero;
              }

              let newZero = 0;
              if (data.results[0].zero !== undefined && data.results[0].zero !== null)
              {
                newZero = data.results[0].zero;
              }

              zero = previousZero + newZero;
            }

            // return the updated counts
            return {
            up:   p.up   + data.results[0].up,
            down: p.down + data.results[0].down,
            zero: zero,
          };
        });
       }

      // if the network request failed, log the error and skip this tick
      catch (err)
      {
        console.error(err);
      }
    };

      const interval = setInterval(tick, streamSpeed);
      return () => clearInterval(interval);
    }, [streaming, streamSpeed, buildPythonPackage, spinType]);

    //percentages, updated so they are now a total percentage of the amount of atoms from the source instead of as percentage of the final amount
    let total = 0;
    if (result)
    {
      total = result.up + result.down + (result.zero ?? 0);
    }

    let upPct = 0;
    if (total > 0)
    {
      upPct = (result!.up / atoms) * 100;
    }

    let downPct = 0;
    if (total > 0)
    {
      downPct = (result!.down / atoms) * 100;
    }

    let zeroPct = 0;
    if (total > 0 && spinType === "1")
    {
      zeroPct = ((result!.zero ?? 0) / atoms) * 100;
    }


    return (
      <div className={loading ? "app-loading" : ""}>
        {/* Config row */}
        <div className="beamline">
          <div className="box config-box">
            <p>Spin type</p>
            <div className="button-group">
              {(["1/2", "1"] as SpinType[]).map(s => (
                <button key={s} className={spinType === s ? "active" : ""} onClick={() => { setActiveDemo(null); setSpinType(s); }}>
                  {s}
                </button>
              ))}
            </div>
          </div>

          <div className="box config-box">
            <p>How many analysers</p>
            <div className="button-group">
              {[1, 2, 3].map(n => (
                <button key={n} className={numAnalysers === n ? "active" : ""} onClick={() => { setActiveDemo(null); setNumAnalysers(n); }}>
                  {n}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Main beamline */}
        <div className="beamline">

          {/* Source */}
          <div className="box-container">
            <div className="box source">
              <p>Source</p>
              {streaming ? (
                <p>Particles fired: {particlesFired}</p>
              ) : (
                <input
                  type="number"
                  value={atoms}
                  onChange={e => setAtoms(parseInt(e.target.value))}
                />
              )}
              {loading && (
                <p className="preparing-msg">Preparing state...</p>
              )}
              {normWarning && (
                <p className="norm-warning">State Normalised!</p>
              )}
              <div className="state-type-toggle">
                <button className={stateType === "R" ? "active" : ""} onClick={() => setStateType("R")}>R</button>
                <button
                  className={stateType === "ψ" ? "active" : ""}
                  onClick={() => { setStateType("ψ"); setShowCalculator(true); }}
                >
                  ψ
                </button>
              </div>

              <div className="speed-control">
                <label>Speed:</label>
                <div className="speed-selector-wrapper">
                  <div className="speed-box" onClick={() => setOpenSpeedDropdown(v => !v)}>
                    {Speed_label[streamSpeed] ?? "Custom"}
                  </div>
                  {openSpeedDropdown && (
                    <div className="speed-dropdown">
                      {Particle_flow_speed.map(({ label, value }) => (
                        <div
                          key={value}
                          className="speed-option"
                          onClick={() => { setStreamSpeed(value); setOpenSpeedDropdown(false); }}
                        >
                          {label}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
            <div className="source-beam" />
          </div>

          {/* Analysers */}
          {analysers.map((an, idx) => (
            <div className="box-container" key={idx}>
              <div className="box analyser">
                <div className="analyser-content">

                  {/* Axis dropdown */}
                  <div className="axis-selector-wrapper">
                    <div
                      className="axis-box"
                      onClick={() => setOpenAxisDropdown(openAxisDropdown === idx ? null : idx)}
                    >
                      {an.axis.toUpperCase()}
                    </div>
                    {openAxisDropdown === idx && (
                      <div className="axis-dropdown">
                        {AXES.map(axis => (
                          <div
                            key={axis}
                            className="axis-option"
                            onClick={() => { updateAnalyserConfig(idx, { axis }); setOpenAxisDropdown(null); }}
                          >
                            {axis.toUpperCase()}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>

                  {/* Spin toggles */}
                  <div className="spin-choice">
                    <div className={`block ${an.upSelected ? "active" : "inactive"}`} onClick={() => changePathChoice(idx, "up")}>↑</div>
                    {spinType === "1" && (
                      <div className={`block ${an.zeroSelected ? "active" : "inactive"}`} onClick={() => changePathChoice(idx, "zero")}>0</div>
                    )}
                    <div className={`block ${an.downSelected ? "active" : "inactive"}`} onClick={() => changePathChoice(idx, "down")}>↓</div>
                  </div>
                </div>

                {/* θ/φ inputs */}
                {an.axis === "θ/φ" && (
                  <div className="theta-phi-inputs">
                    {(["theta", "phi"] as const).map(field => (
                      <div className="angle-input-group" key={field}>
                        <label>{field === "theta" ? "θ" : "φ"}</label>
                        <input
                          className="angle-input"
                          type="text"
                          value={an[field] ?? "0"}
                          onChange={e => updateAnalyserConfig(idx, { [field]: e.target.value })}
                        />
                        {/* π button — appends π to the field; presence of π triggers radian mode */}
                        <button
                          className="pi-button"
                          onClick={() => appendPi(idx, field)}
                          title="Insert π (switches input to radians)"
                        >
                          π
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className={`connectors ${spinType === "1/2" ? "spin-half" : "spin-one"}`}>
                <div className={`connector up   ${!an.upSelected   ? "hidden-connector" : ""}`} />
                {spinType === "1" && (
                  <div className={`connector zero ${!an.zeroSelected ? "hidden-connector" : ""}`} />
                )}
                <div className={`connector down  ${!an.downSelected ? "hidden-connector" : ""}`} />
              </div>
            </div>
          ))}

          {/* Detector */}
          <div className="box-container">
            <div className="box detector">
              <p>Detector</p>
              <div className="detector-controls">
                <button onClick={runMeasurement} disabled={loading || streaming}>
                  {loading ? "Running..." : "Run"}
                </button>
                <button onClick={() => {
                  if (!streaming) setLoading(true);
                  setStreaming(v => !v);
                }}>
                  {streaming ? "Stop" : "Start"}
                </button>  
                <button onClick={() => {setResult(null); setParticlesFired(0); setNormWarning(false);}}>Reset</button>
              </div>
              {result && (
                <>
                  <div className="result">
                    <strong>Final Count:</strong> ↑ {result.up}
                    {spinType === "1" && <> | 0 {result.zero}</>}
                    {" "}| ↓ {result.down}
                  </div>
                  <div className="probability-bars">
                    {[
                      { label: "↑",  pct: upPct,   cls: "up"   },
                      ...(spinType === "1" ? [{ label: "0", pct: zeroPct, cls: "zero" }] : []),
                      { label: "↓",  pct: downPct,  cls: "down" },
                    ].map(({ label, pct, cls }) => (
                      <div className="bar-row" key={cls}>
                        <span className="bar-label">{label}</span>
                        <div className="bar-track">
                          {pct > 0 && (
                            <div className={`bar-fill ${cls}`} style={{ width: `${pct}%` }}>
                              <span className="bar-text">{pct.toFixed(1)}%</span>
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </>
              )}
            </div>
          </div>
        </div>

        {showCalculator && (
          <CalculatorModal
            spinType={spinType}
            aValue={coeffs.a}
            bValue={coeffs.b}
            cValue={coeffs.c ?? ""}
            setAValue={a => setCoeffs(prev => ({ ...prev, a }))}
            setBValue={b => setCoeffs(prev => ({ ...prev, b }))}
            setCValue={c => setCoeffs(prev => ({ ...prev, c }))}
            onClose={() => setShowCalculator(false)}
          />
        )}
        <div style={{ textAlign: "center" }}>
          <button className="collapse-toggle" onClick={() => setBottomOpen(v => !v)}>
            {bottomOpen ? "▲ Close instructions" : "▼ Open Instructions"}
          </button>
        </div>

        {bottomOpen && (
          <div className="bottom-row">
            <div className="instructions-box">
              {activeDemo !== null ? (
                <>
                  <h3>{activeDemo.description.title}</h3>

                  <h4>Setup</h4>
                  <ul>
                    {activeDemo.description.setup.map((point, i) => (
                      <li key={i}>{point}</li>
                    ))}
                  </ul>

                  <h4>What to observe</h4>
                  <ul>
                    {activeDemo.description.observe.map((point, i) => (
                      <li key={i}>{point}</li>
                    ))}
                  </ul>

                  <h4>Why does this happen?</h4>
                  <p>{activeDemo.description.explanation}</p>
                </>
              ) : (
                <Instructions/>
              )}
            
            </div>

            <div className="test-cases-box">
              <p>Experiements</p>
              <div className="button-group">
                <button onClick={resetSimulator}>
                    Reset Simulator
                </button>
              </div>
              <div className="button-group">
                {demonstationCases.map((demo, index) => (
                  <button
                    key={demo.label}
                    onClick={() => ApplyDemo(demo)}
                  >
                    {demo.label}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>      
    );           
  }      
export default SternGerlachSim;
