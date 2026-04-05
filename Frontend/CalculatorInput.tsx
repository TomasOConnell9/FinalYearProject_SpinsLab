import { useState, useEffect, useCallback } from "react";
import "./App.css";

interface CalculatorModalProps {
  spinType: "1/2" | "1";
  aValue: string;
  bValue: string;
  cValue: string;
  setAValue: (val: string) => void;
  setBValue: (val: string) => void;
  setCValue: (val: string) => void;
  onClose: () => void;
}

export default function CalculatorModal({
  spinType, aValue, bValue, cValue,
  setAValue, setBValue, setCValue, onClose,
}: CalculatorModalProps) {
  const [target, setTarget] = useState<"a" | "b" | "c">("a");

  const handleButton = useCallback((char: string) => {
    const insertChar = (c: string) => {
      const val = c === "√" ? "√(" : c;
      if (target === "a") setAValue(aValue + val);
      else if (target === "b") setBValue(bValue + val);
      else setCValue(cValue + val);
    };
    const clear = () => {
      if (target === "a") setAValue("");
      else if (target === "b") setBValue("");
      else setCValue("");
    };
    if (char === "C") clear();
    else if (char === "⌫") {
      if (target === "a") setAValue(aValue.slice(0, -1));
      else if (target === "b") setBValue(bValue.slice(0, -1));
      else setCValue(cValue.slice(0, -1));
    } else {
      insertChar(char);
    }
  }, [target, aValue, bValue, cValue, setAValue, setBValue, setCValue]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const handledKeys = ['0','1','2','3','4','5','6','7','8','9',
                           '+','-','*','/','.','^','(',')',
                           'Backspace','Delete','Escape','Enter','Tab'];
      if (handledKeys.includes(e.key) ||
          (e.key.toLowerCase() === 'p' && !e.ctrlKey) ||
          (e.key.toLowerCase() === 'c' && !e.ctrlKey) ||
          (e.key.toLowerCase() === 's')) {
        e.preventDefault();
      }
      if (/^[0-9]$/.test(e.key)) handleButton(e.key);
      else if (e.key === '+') handleButton('+');
      else if (e.key === '-') handleButton('-');
      else if (e.key === '*') handleButton('*');
      else if (e.key === '/') handleButton('/');
      else if (e.key === '^') handleButton('^');
      else if (e.key === '.') handleButton('.');
      else if (e.key === '(' || e.key === '[') handleButton('(');
      else if (e.key === ')' || e.key === ']') handleButton(')');
      else if (e.key.toLowerCase() === 'i') handleButton('i');
      else if (e.key.toLowerCase() === 'e') handleButton('e');
      else if (e.key.toLowerCase() === 'p') handleButton('π');
      else if (e.key.toLowerCase() === 's') handleButton('√');
      else if (e.key === 'Backspace') handleButton('⌫');
      else if (e.key === 'Delete') handleButton('⌫');
      else if (e.key.toLowerCase() === 'c' && !e.ctrlKey) handleButton('C');
      else if (e.key === 'Tab') {
        if (target === "a") setTarget("b");
        else if (target === "b") setTarget(spinType === "1" ? "c" : "a");
        else setTarget("a");
      }
      else if (e.key === 'Escape' || e.key === 'Enter') onClose();
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [target, spinType, onClose, handleButton]);

  const buttons = [
    "7","8","9","/","√",
    "4","5","6","*","^",
    "1","2","3","+","-",
    "0","i",".","(",")",
    "e","π","C","⌫",
  ];

  return (
    <div className="modal-overlay">
      <div className="modal calculator-modal">
        <h3>Prepare your quantum state</h3>
        <div className="quantum-display">
          {spinType === "1/2" ? (
            <>|ψ⟩ = (<span className="amp">{aValue || "0"}</span>)&nbsp;|↑⟩&nbsp;+&nbsp;(<span className="amp">{bValue || "0"}</span>)&nbsp;|↓⟩</>
          ) : (
            <>|ψ⟩ = (<span className="amp">{aValue || "0"}</span>)&nbsp;|1⟩&nbsp;+&nbsp;(<span className="amp">{bValue || "0"}</span>)&nbsp;|0⟩&nbsp;+&nbsp;(<span className="amp">{cValue || "0"}</span>)&nbsp;|-1⟩</>
          )}
        </div>
        <div className="target-select">
          <button onClick={() => setTarget("a")} className={target === "a" ? "active" : ""}>{spinType === "1/2" ? "|↑⟩" : "|1⟩"}</button>
          <button onClick={() => setTarget("b")} className={target === "b" ? "active" : ""}>{spinType === "1/2" ? "|↓⟩" : "|0⟩"}</button>
          {spinType === "1" && <button onClick={() => setTarget("c")} className={target === "c" ? "active" : ""}>|-1⟩</button>}
        </div>
        <div className="display-box">
          {target === "a" ? aValue || " " : target === "b" ? bValue || " " : cValue || " "}
        </div>
        <div className="button-grid">
          {buttons.map((b) => <button key={b} onClick={() => handleButton(b)}>{b}</button>)}
        </div>
        <button className="close-btn" onClick={onClose}>Apply State (Enter)</button>
      </div>
    </div>
  );
}