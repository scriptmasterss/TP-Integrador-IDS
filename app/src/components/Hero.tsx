import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

const Hero: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="px-12 py-10 relative">
      <motion.div 
        initial={{ scale: 0.98, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="relative w-full h-[450px] border-[2px] border-[#1a73e8] bg-white flex items-center justify-between px-20 rounded-2xl shadow-[0_15px_40px_rgba(26,115,232,0.2)] group transition-all duration-500 overflow-hidden"
      >
        {/* Background Image from User */}
        <div 
          className="absolute inset-0 bg-cover bg-center transition-transform duration-1000 group-hover:scale-105"
          style={{ 
            backgroundImage: `url('/hero-bg.png')`,
          }}
        />
        
        {/* Darker Overlay for better text readability */}
        <div className="absolute inset-0 bg-black/40 group-hover:bg-black/30 transition-colors duration-500" />

        <div className="flex flex-col gap-10 relative z-10">
          <div className="text-[56px] font-[900] text-white leading-[1] tracking-tight drop-shadow-2xl">
            ¡Solicita lo<br />que<br />
            <span className="text-[#64b5f6] relative">
              necesites!
              <motion.div 
                initial={{ width: 0 }}
                animate={{ width: '100%' }}
                transition={{ duration: 0.8, delay: 0.8 }}
                className="absolute -bottom-2 left-0 h-[4px] bg-[#64b5f6]/50 rounded-full"
              />
            </span>
          </div>
        </div>
        
        <div className="flex items-center relative z-10">
          <motion.button 
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => navigate('/login')}
            className="text-white text-[15px] font-black tracking-[2px] border-2 border-white/50 hover:border-white hover:text-white px-10 py-5 rounded-full cursor-pointer bg-black/20 backdrop-blur-md transition-all duration-300 uppercase shadow-xl"
          >
            RESERVA AQUÍ
          </motion.button>
        </div>
      </motion.div>
    </div>
  );
};

export default Hero;
