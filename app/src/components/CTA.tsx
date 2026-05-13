import React from 'react';
import { useNavigate } from 'react-router-dom';

const CTA: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="text-center bg-white py-[100px] px-[40px] border-t border-[#f0f0f0]">
      <h2 className="text-[36px] font-black mb-[40px] text-[#111] tracking-tight">Registrate ahora!</h2>
      <button 
        onClick={() => navigate('/login')}
        className="text-[#aaa] text-[15px] font-black border-2 border-[#eee] hover:border-[#1a73e8] hover:text-[#1a73e8] bg-transparent px-16 py-4 rounded-full cursor-pointer tracking-[2px] transition-all duration-300 uppercase shadow-sm hover:shadow-lg"
      >
        INGRESA
      </button>
    </div>
  );
};

export default CTA;
