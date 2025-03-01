import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Login from './components/Login';
import LogList from './components/LogList';

function App() {
    return (
        <div className="App">
            <h1 className='header'>سیستم مدیریت لاگ‌ها</h1>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/logs" element={<LogList />} />
            </Routes>
        </div>
    );
}

export default App;