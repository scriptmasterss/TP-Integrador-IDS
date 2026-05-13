import Navbar from './Navbar';
import Hero from './Hero';
import HowItWorks from './HowItWorks';
import Benefits from './Benefits';
import Norms from './Norms';
import FAQ from './FAQ';
import CTA from './CTA';
import Footer from './Footer';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';

const LandingPage: React.FC = () => {
  const navigate = useNavigate();

  const handleLoginClick = () => {
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-[#fcfcfc] flex justify-center py-[60px] font-sans text-[#111] selection:bg-[#1a73e8] selection:text-white">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-[900px] bg-white shadow-[0_20px_50px_rgba(0,0,0,0.05)] overflow-hidden border border-[#f0f0f0] rounded-xl"
      >
        <Navbar onLoginClick={handleLoginClick} />
        <Hero />
        <div className="space-y-12 pb-20">
          <HowItWorks />
          <Benefits />
          <Norms />
          <FAQ />
          <CTA />
        </div>
        <Footer />
      </motion.div>
    </div>
  );
};

export default LandingPage;
