import React, { useState } from 'react';

const FAQ: React.FC = () => {
  const [openIndices, setOpenIndices] = useState<number[]>([0, 1, 2]);

  const faqs = [
    {
      q: '¿Cómo cancelo una reserva?',
      a: 'Podés hacerlo desde tu perfil de alumno o mediante el botón "Cancelar" incluido en el mail de confirmación del QR.'
    },
    {
      q: '¿Qué pasa si pierdo el código QR?',
      a: 'No te preocupes, podés volver a generarlo o visualizarlo ingresando con tu usuario y contraseña a la plataforma.'
    },
    {
      q: '¿Puedo renovar una reserva activa?',
      a: 'Sí, siempre y cuando no haya otros alumnos en lista de espera para ese mismo objeto.'
    }
  ];

  const toggle = (idx: number) => {
    if (openIndices.includes(idx)) {
      setOpenIndices(openIndices.filter(i => i !== idx));
    } else {
      setOpenIndices([...openIndices, idx]);
    }
  };

  return (
    <section className="bg-white py-[80px] px-[80px]">
      <h2 className="text-center text-[28px] font-bold mb-[60px] text-[#111]">FAQ</h2>
      <div className="flex flex-col gap-6">
        {faqs.map((faq, idx) => {
          const isOpen = openIndices.includes(idx);
          return (
            <div
              key={idx}
              className={`border-[1.5px] rounded-[2px] overflow-hidden ${
                isOpen ? 'border-[#1a73e8]' : 'border-[#ddd]'
              }`}
            >
              <div
                className="flex items-center justify-between p-[18px] px-[22px] text-[13px] font-bold cursor-pointer bg-white"
                onClick={() => toggle(idx)}
              >
                <div className="flex items-center">
                  <span className="text-[#111] text-[18px] mr-[15px]">
                    {isOpen ? '−' : '+'}
                  </span>
                  {faq.q}
                </div>
                <span className="text-[#111] text-[14px]">
                  {isOpen ? '∧' : '∨'}
                </span>
              </div>
              {isOpen && (
                <div className="p-[0_22px_18px_55px] text-[12px] text-[#555] font-medium leading-[1.8]">
                  {faq.a}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
};

export default FAQ;
