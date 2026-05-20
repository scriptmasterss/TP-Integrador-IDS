import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-[#171717] border-t-2 border-[#1a73e8] py-16 px-20 flex flex-col gap-12">
      <div className="flex items-center justify-between">
        {/* Literal High Definition Logo Integration */}
        <div className="flex items-center bg-white p-2 rounded-lg">
          <a href="https://www.fi.uba.ar/" target="_blank" rel="noopener noreferrer">
            <img 
              src="/logo-fiuba.png" 
              alt="UBAfiuba Facultad de Ingeniería" 
              className="h-24 w-auto object-contain"
              style={{ minWidth: '320px' }}
              onError={(e) => {
                const target = e.currentTarget;
                target.style.display = 'none';
                const container = target.parentElement;
                if (container) {
                  container.innerHTML = `
                    <div class="flex flex-col">
                      <div style="font-size: 36px; font-weight: 900; color: #111; letter-spacing: -1px;">.UBA<span style="color: #1a73e8;">fiuba</span></div>
                      <div style="font-size: 11px; font-weight: 800; color: #111; letter-spacing: 0.25em; text-transform: uppercase; margin-top: 4px;">Facultad de Ingeniería</div>
                    </div>`;
                }
              }}
            />
          </a>
        </div>

        {/* Social Media Icons Decorated with generic labels */}
        <div className="flex items-center gap-4">
          {[
            { label: 'f', color: 'hover:bg-blue-600' },
            { label: '𝕏', color: 'hover:bg-black' },
            { label: 'ig', color: 'hover:bg-pink-600' },
            { label: 'in', color: 'hover:bg-blue-700' },
            { label: 'yt', color: 'hover:bg-red-600' }
          ].map((social, idx) => (
            <a 
              key={idx}
              href="#" 
              className={`w-11 h-11 rounded-full border-2 border-[#444] flex items-center justify-center text-white hover:text-white transition-all duration-300 transform hover:-translate-y-1 hover:shadow-lg ${social.color} font-black select-none text-[15px]`}
            >
              {social.label}
            </a>
          ))}
        </div>
      </div>

      <div className="flex items-center justify-between pt-10 border-t border-[#333] text-[13px] text-white font-black uppercase tracking-[0.15em]">
        <div className="flex items-center gap-3">
          <div className="w-2.5 h-2.5 rounded-full bg-[#1a73e8] shadow-[0_0_10px_rgba(26,115,232,0.6)]" />
          © 2026 FIUBA - Todos los derechos reservados
        </div>
        <div className="flex gap-12 font-black">
          <a href="#" className="text-white hover:text-[#1a73e8] transition-colors">Aviso Legal</a>
          <a href="#" className="text-white hover:text-[#1a73e8] transition-colors">Privacidad</a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
