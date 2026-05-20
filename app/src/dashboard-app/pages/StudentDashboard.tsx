import { useNavigate } from "react-router-dom";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";
import { BookOpen, Search, Clock, Package, AlertCircle, User, LogOut, ChevronRight } from "lucide-react";
import { motion } from "framer-motion";

export function StudentDashboard() {
  const navigate = useNavigate();

  const activeLoan = {
    id: "PR-2024-001",
    item: "Computadora Portátil Dell",
    dueDate: "2026-05-15",
    status: "active"
  };

  const recentItems = [
    { id: 1, name: "Arduino UNO R3", category: "Placas", available: 12 },
    { id: 2, name: "Análisis Matemático I - Protter", category: "Libros", available: 5 },
    { id: 3, name: "Proyector Epson EB-X41", category: "Proyectores", available: 3 },
    { id: 4, name: "Cable HDMI 2.0 (3m)", category: "Cables", available: 24 },
  ];

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1 }
  };

  return (
    <div className="min-h-screen bg-[#fcfcfc] selection:bg-[#1a73e8] selection:text-white">
      {/* Decorated Header */}
      <header className="bg-white border-b-2 border-[#1a73e8] sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-8 py-5 flex items-center justify-between">
          <div className="flex items-center gap-6">
            <div className="bg-[#1a73e8] p-3 rounded-2xl shadow-lg shadow-blue-200">
              <BookOpen className="w-7 h-7 text-white" />
            </div>
            <div className="flex flex-col">
              <h1 className="font-black text-2xl text-[#111] tracking-tight">Panel Biblioteca</h1>
              <div className="flex items-center gap-2 text-xs font-bold text-[#1a73e8] uppercase tracking-widest">
                <User className="w-3 h-3" /> Juan Pérez
              </div>
            </div>
          </div>
          <Button 
            variant="ghost" 
            onClick={() => navigate("/")}
            className="group flex items-center gap-2 font-bold text-[#888] hover:text-red-500 hover:bg-red-50 transition-colors py-6 px-6 rounded-xl"
          >
            <LogOut className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
            Cerrar Sesión
          </Button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-8 py-12">
        <motion.div 
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="space-y-12"
        >
          {/* Main Action Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { title: "Buscar Material", icon: Search, path: "/buscar", desc: "Explora libros y equipos", color: "text-blue-600", bg: "bg-blue-50" },
              { title: "Mis Préstamos", icon: Package, path: "/historial", desc: "Historial y activos", color: "text-purple-600", bg: "bg-purple-50" },
              { title: "Normas", icon: AlertCircle, path: "/", desc: "Reglamento vigente", color: "text-amber-600", bg: "bg-amber-50" }
            ].map((card, i) => (
              <motion.div key={i} variants={itemVariants} whileHover={{ y: -8 }}>
                <Card 
                  className="cursor-pointer border-2 border-transparent hover:border-[#1a73e8] shadow-[0_10px_30px_rgba(0,0,0,0.03)] hover:shadow-xl transition-all duration-300 rounded-2xl overflow-hidden h-full group" 
                  onClick={() => navigate(card.path)}
                >
                  <CardHeader className="p-8">
                    <div className={`${card.bg} w-16 h-16 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform`}>
                      <card.icon className={`w-8 h-8 ${card.color}`} />
                    </div>
                    <CardTitle className="text-2xl font-black text-[#111] mb-2">{card.title}</CardTitle>
                    <CardDescription className="text-sm font-medium text-[#888]">{card.desc}</CardDescription>
                  </CardHeader>
                </Card>
              </motion.div>
            ))}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Active Loan Section */}
            <motion.div variants={itemVariants} className="lg:col-span-1">
              <div className="flex items-center gap-3 mb-6">
                <Clock className="w-5 h-5 text-[#1a73e8]" />
                <h2 className="text-[18px] font-black uppercase tracking-wider text-[#111]">Préstamo Activo</h2>
              </div>
              <Card className="border-2 border-[#1a73e8] bg-white shadow-xl rounded-2xl overflow-hidden relative">
                <div className="absolute top-0 left-0 w-1.5 h-full bg-[#1a73e8]" />
                <CardHeader className="p-8">
                  <Badge className="w-fit bg-[#1a73e8] hover:bg-[#1a73e8] text-white px-3 py-1 rounded-full font-bold mb-4">ACTIVO</Badge>
                  <CardTitle className="text-xl font-black text-[#111] mb-4">{activeLoan.item}</CardTitle>
                  <div className="space-y-4">
                    <div className="flex justify-between text-sm items-center py-3 border-b border-gray-100">
                      <span className="text-[#888] font-bold">FECHA LÍMITE</span>
                      <span className="text-red-500 font-black">{activeLoan.dueDate}</span>
                    </div>
                    <div className="flex justify-between text-sm items-center py-3">
                      <span className="text-[#888] font-bold">ID RESERVA</span>
                      <span className="text-[#111] font-mono font-bold">{activeLoan.id}</span>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="px-8 pb-8 pt-0">
                  <Button className="w-full bg-[#111] hover:bg-[#333] text-white font-bold h-12 rounded-xl">
                    Ver Código QR
                  </Button>
                </CardContent>
              </Card>
            </motion.div>

            {/* Catalog Section */}
            <motion.div variants={itemVariants} className="lg:col-span-2">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <Package className="w-5 h-5 text-[#1a73e8]" />
                  <h2 className="text-[18px] font-black uppercase tracking-wider text-[#111]">Disponibilidad</h2>
                </div>
                <button className="text-[13px] font-black text-[#1a73e8] hover:underline flex items-center gap-1">
                  Ver Catálogo Completo <ChevronRight className="w-4 h-4" />
                </button>
              </div>
              <Card className="border border-gray-100 shadow-[0_10px_30px_rgba(0,0,0,0.03)] rounded-2xl overflow-hidden">
                <div className="divide-y divide-gray-100">
                  {recentItems.map((item) => (
                    <div 
                      key={item.id} 
                      className="p-6 flex items-center justify-between hover:bg-gray-50 transition-colors group cursor-pointer"
                      onClick={() => navigate(`/prestamo/${item.id}`)}
                    >
                      <div className="flex items-center gap-6">
                        <div className="w-12 h-12 bg-gray-100 rounded-xl flex items-center justify-center font-black text-[#888]">
                          {item.id}
                        </div>
                        <div>
                          <h3 className="font-bold text-[#111] group-hover:text-[#1a73e8] transition-colors">{item.name}</h3>
                          <p className="text-[11px] font-bold text-[#aaa] uppercase tracking-wider">{item.category}</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-4">
                        <Badge variant="secondary" className="font-bold px-3 py-1 bg-green-50 text-green-700 hover:bg-green-50 border-none">
                          {item.available} DISPONIBLES
                        </Badge>
                        <ChevronRight className="w-5 h-5 text-[#ddd] group-hover:text-[#1a73e8] transform group-hover:translate-x-1 transition-all" />
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
            </motion.div>
          </div>
        </motion.div>
      </main>
    </div>
  );
}
