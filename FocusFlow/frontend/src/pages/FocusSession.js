import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Timer from '../components/Timer';
import './FocusSession.css';  // Make sure to create this CSS file

function FocusSession() {
  const navigate = useNavigate();
  const [duration, setDuration] = useState(25 * 60);
  const [customMinutes, setCustomMinutes] = useState(25);
  const [isRunning, setIsRunning] = useState(false);
  const [tasks, setTasks] = useState([]);
  const [taskInput, setTaskInput] = useState('');

  useEffect(() => {
    const storedTasks = localStorage.getItem('tasks');
    if (storedTasks) setTasks(JSON.parse(storedTasks));
  }, []);

  useEffect(() => {
    localStorage.setItem('tasks', JSON.stringify(tasks));
  }, [tasks]);

  const handleAddTask = () => {
    if (taskInput.trim()) {
      setTasks([...tasks, { text: taskInput.trim(), completed: false }]);
      setTaskInput('');
    }
  };

  const toggleTaskCompletion = (index) => {
    const updatedTasks = [...tasks];
    updatedTasks[index].completed = !updatedTasks[index].completed;
    setTasks(updatedTasks);
  };

  const deleteTask = (index) => {
    const updatedTasks = tasks.filter((_, i) => i !== index);
    setTasks(updatedTasks);
  };

  const startTimer = () => {
    setDuration(customMinutes * 60);
    setIsRunning(true);
  };

  return (
    <div className="container" style={{ position: 'relative' }}>
      {/* Return to Home Button */}
      <button
        onClick={() => navigate('/')}
        style={{
          position: 'absolute',
          top: '10px',
          left: '10px',
          padding: '5px 10px',
          fontSize: '12px',
          borderRadius: '5px',
          border: 'none',
          backgroundColor: '#ccc',
          cursor: 'pointer',
        }}
      >
        ⬅ Home
      </button>

      <h2>Focus Session</h2>

      <div className="timer-settings">
        <label>
          Set Duration (minutes): 
          <input
            type="number"
            min="1"
            max="180"
            value={customMinutes}
            onChange={(e) => setCustomMinutes(Number(e.target.value))}
          />
        </label>
        <button className="btn" onClick={startTimer}>Start Session</button>
      </div>

      {isRunning && (
        <div style={{ position: 'relative', marginTop: '20px', height: '50px' }}>
          <Timer
            duration={duration}
            onFinish={() => alert('Focus session complete!')}
          />

          <div className="cycling-animation">
            🚴‍♂️
          </div>
        </div>
      )}

      <div className="todo-list">
        <h3>📝 To-Do Tasks</h3>
        <div className="task-input">
          <input
            type="text"
            placeholder="Add a new task..."
            value={taskInput}
            onChange={(e) => setTaskInput(e.target.value)}
          />
          <button className="btn" onClick={handleAddTask}>Add Task</button>
        </div>

        <ul>
          {tasks.map((task, index) => (
            <li
              key={index}
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                cursor: 'pointer',
                textDecoration: task.completed ? 'line-through' : 'none'
              }}
            >
              <span onClick={() => toggleTaskCompletion(index)}>
                {task.text} {task.completed && '(Finished)'}
              </span>
              <button
                onClick={() => deleteTask(index)}
                style={{
                  background: 'red',
                  color: 'white',
                  border: 'none',
                  borderRadius: '50%',
                  width: '20px',
                  height: '20px',
                  cursor: 'pointer',
                  fontWeight: 'bold'
                }}
              >
                ×
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default FocusSession;
