import { useState, useEffect } from 'react';

function Timer({ duration, onFinish }) {
  const [timeLeft, setTimeLeft] = useState(duration);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    if (timeLeft <= 0) {
      onFinish();
      return;
    }

    const timerId = setTimeout(() => {
      setTimeLeft(timeLeft - 1);
      setProgress(((duration - (timeLeft - 1)) / duration) * 100);
    }, 1000);

    return () => clearTimeout(timerId);
  }, [timeLeft, duration]);

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div>
      <div className="timer">{formatTime(timeLeft)}</div>
      <div className="progress-bar">
        <div
          className="progress-bar-fill"
          style={{ width: `${progress}%` }}
        ></div>
      </div>
    </div>
  );
}

export default Timer;
