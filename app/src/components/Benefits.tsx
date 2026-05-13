import React from 'react';
import { ThumbsUp, Laptop, Mail } from 'lucide-react';
import { motion } from 'framer-motion';

const Benefits: React.FC = () => {
  const benefits = [
    { icon: <ThumbsUp className="w-8 h-8 text-[#1a73e8]" />, name: 'Beneficio 1', desc: 'Retiro inmediato con QR.' },
    { icon: <Laptop className="w-8 h-8 text-[#1a73e8]" />, name: 'Beneficio 2', desc: 'Acceso a notebooks y proyectores.' },
    { icon: <Mail className="w-8 h-8 text-[#1a73e8]" />, name: 'Beneficio 3', desc: 'Notificaciones de devolución por\nmail' }
  ];

  return (
    <section className="bg-white py-[60px] px-[40px]">
      <h2 className="text-center text-[32px] font-bold mb-[60px] text-[#111]">¿Por qué solicitar una reserva?</h2>
      <div className="flex justify-around gap-[40px] px-12">
        {benefits.map((benefit, idx) => (
          <motion.div 
            key={idx} 
            whileHover={{ y: -5 }}
            className="flex-1 text-center flex flex-col items-center group"
          >
            <div className="w-20 h-20 bg-gray-50 rounded-2xl flex items-center justify-center mb-6 transition-colors group-hover:bg-blue-50">
              {benefit.icon}
            </div>
            <div className="text-[15px] font-bold mb-3 text-[#111]">{benefit.name}</div>
            <div className="text-[12px] text-[#666] leading-[1.6] font-medium max-w-[180px] whitespace-pre-line">{benefit.desc}</div>
          </motion.div>
        ))}
      </div>
    </section>
  );
};

export default Benefits;
