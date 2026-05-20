import React from 'react';

interface NavbarProps {
  onLoginClick?: () => void;
}

const Navbar: React.FC<NavbarProps> = ({ onLoginClick }) => {
  return (
    <nav className="flex items-center justify-between px-10 py-8 bg-white border-b border-[#f0f0f0]">
      <div className="text-2xl font-bold text-[#111] tracking-tight">
        Biblioteca <span className="text-[#1a73e8]">Fiuba</span>
      </div>
      
      <div className="flex items-center gap-12">
        <div className="flex gap-10 text-[13px] text-[#333] items-center">
          <a href="#" className="text-center leading-tight hover:text-[#1a73e8] transition-colors font-bold uppercase tracking-wider">
            Información<br />general
          </a>
          <a href="#" className="hover:text-[#1a73e8] transition-colors font-bold uppercase tracking-wider">
            Recursos<br />digitales
          </a>
          <a href="#" className="hover:text-[#1a73e8] transition-colors font-bold uppercase tracking-wider">
            Servicios
          </a>
          <a href="#" className="hover:text-[#1a73e8] transition-colors font-bold uppercase tracking-wider">
            Catálogo
          </a>
        </div>
        
        <button
          onClick={onLoginClick}
          className="text-[#aaa] text-[13px] font-black tracking-widest uppercase hover:text-[#1a73e8] hover:border-[#1a73e8] transition-all bg-transparent border-2 border-[#eee] px-6 py-3 rounded-lg cursor-pointer"
        >
          INICIA SESIÓN
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
