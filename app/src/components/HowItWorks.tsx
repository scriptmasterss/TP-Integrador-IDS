import React from 'react';

const HowItWorks: React.FC = () => {
  const steps = [
    {
      num: '01',
      name: 'Ingresá a\nnuestro\ncatálogo',
      desc: 'Allí podrás ver con lo que contamos',
    },
    {
      num: '02',
      name: 'Solicitá tu\nreserva',
      desc: 'Te solicitaremos unos datos por seguridad de la facultad',
    },
    {
      num: '03',
      name: 'Envío de QR y\nconfirmación\nvía mail',
      desc: '¡Listo con la confirmación generada podrás retirarlo en la librería!',
    }
  ];

  return (
    <section className="py-[60px] px-[40px] bg-black/80 text-white">
      <h2 className="text-center text-[28px] font-bold mb-[10px] text-white">¿Cómo funciona?</h2>
      <p className="text-center text-[13px] text-white/70 mb-[60px] font-medium">¡A continuación de dejamos los pasos a seguir!</p>
      
      <div className="flex justify-between items-start gap-[40px] relative px-10 text-white">
        {steps.map((step, idx) => (
          <div key={idx} className="flex-1 text-center flex flex-col items-center">
            <div className="w-[50px] h-[50px] border border-white/30 rounded-full flex items-center justify-center font-normal text-[14px] text-white/80 mb-[20px] bg-white/10">
              {step.num}
            </div>
            <div className="text-[14px] font-bold mb-[10px] leading-[1.3] whitespace-pre-line text-white">
              {step.name}
            </div>
            <div className="text-[11px] text-white/60 leading-[1.5] font-medium max-w-[160px]">
              {step.desc}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default HowItWorks;
