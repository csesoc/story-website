import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import 'bootstrap/dist/css/bootstrap.min.css';

import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from './pages/Register';
import About from './pages/About';
import Leaderboard from './pages/Leaderboard';
import Calendar from './pages/Calendar';
import Stats from './pages/Stats';
import Header from './components/Header';
import Footer from './components/Footer';

const App: React.FC<{}> = () => {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<Navigate to="/2022/" />} />
        <Route path="/2022/" element={<Home />} />
        <Route path="/2022/auth/login" element={<Login />} />
        <Route path="/2022/auth/register" element={<Register />} />
        <Route path="/2022/about" element={<About />} />
        <Route path="/2022/calendar" element={<Calendar />} />
        <Route path="/2022/leaderboard" element={<Leaderboard />} />
        <Route path="/2022/stats" element={<Stats />} />
      </Routes>
      <Footer />
    </Router>
    
  );
}

export default App;
