import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Signup from './screens/Signup';
import Dashboard from './screens/Dashboard'; // Importing the new Dashboard
import DonationHistory from './screens/DonationHistory'
import SignIn from './screens/Sign-in';
import LandingPage from './screens/landingpage';
import CauseListpage from './screens/CauseListpage';
import Donation from './screens/Donation';
import Profilepage from './screens/Profilepage';
import Profilesettings from './screens/profilesettings';
import CartPage from './screens/CartPage';
import MultiDonation from './screens/MultiDonation';
import Notificationspage from './screens/Notificationspage';
import Desktoppage from './screens/Desktoppage';
import CausedetailPage from './screens/CausedetailPage'; // Importing CausedetailPage


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/landingpage" element={<LandingPage />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/sign-in" element={<SignIn />} />
        <Route path="/" element={<Navigate to="/landingpage" replace />} />
        <Route path="/causes" element={<CauseListpage />} />
        <Route path="/donation" element={<Donation />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/donationhistory" element={<DonationHistory />} />
         <Route path="/profilepage" element={<Profilepage />} />
         <Route path="/profilesettings" element={<Profilesettings />} />
         <Route path="/cartpage" element={<CartPage />} />
         <Route path="/multidonation" element={<MultiDonation />} />
         <Route path="/notificationspage" element={<Notificationspage />} />
          <Route path="/desktoppage" element={<Desktoppage />} />
          <Route path="/CausedetailPage" element={<CausedetailPage />} />
      <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
