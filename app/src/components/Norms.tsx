import React from 'react';
import { CheckCircle2 } from 'lucide-react';

const Norms: React.FC = () => {
  const norms = [
    { title: 'Identidad:', text: 'Es obligatorio presentar el QR y el DNI para retirar el material.' },
    { title: 'Devolución:', text: 'El material debe devolverse en el mismo estado y antes de la fecha límite para evitar bloqueos.' },
    { title: 'Estado del Material:', text: 'El usuario es responsable por daños físicos en los equipos técnicos.' },
    { title: 'Multas:', text: 'El retraso o mal estado en la devolución inhabilita al usuario para nuevos préstamos por 15 días.' },
    { title: 'Plazos:', text: 'Las reservas vencen automáticamente si no se retiran en 30 minutos.' },
    { title: 'Seguridad:', text: 'La reserva está protegida para asegurar tus datos.' }
  ];

  return (
    <section className="bg-black/80 py-[60px] px-[80px] text-white">
      <h2 className="text-center text-[32px] font-bold mb-[60px] text-white">Normas</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-x-[60px] gap-y-[40px]">
        {norms.map((norm, idx) => (
          <div key={idx} className="flex gap-[16px] items-start text-[13px] text-white/80 leading-[1.6]">
            <CheckCircle2 className="text-[#64b5f6] w-5 h-5 shrink-0 mt-0.5" />
            <span className="font-medium">
              <strong className="text-white font-bold block mb-1">{norm.title}</strong>
              {norm.text}
            </span>
          </div>
        ))}
      </div>
    </section>
  );
};

export default Norms;
