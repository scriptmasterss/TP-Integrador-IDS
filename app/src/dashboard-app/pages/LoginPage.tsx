import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { BookOpen, ShieldCheck, User } from "lucide-react";
import { motion } from "framer-motion";

export function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = (role: "student" | "admin") => {
    if (role === "student") {
      navigate("/alumno");
    } else {
      navigate("/admin");
    }
  };

  return (
    <div className="min-h-screen bg-[#fcfcfc] flex items-center justify-center p-6 selection:bg-[#1a73e8] selection:text-white">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Card className="w-full max-w-md border-[2px] border-[#1a73e8] shadow-[0_15px_40px_rgba(26,115,232,0.15)] rounded-2xl overflow-hidden bg-white">
          <div className="h-2 bg-[#1a73e8]" />
          <CardHeader className="space-y-4 pt-10 px-10 text-center">
            <div className="mx-auto w-16 h-16 bg-blue-50 rounded-2xl flex items-center justify-center border border-blue-100">
              <BookOpen className="w-8 h-8 text-[#1a73e8]" />
            </div>
            <div className="space-y-1">
              <CardTitle className="text-3xl font-black tracking-tight text-[#111]">Iniciar Sesión</CardTitle>
              <CardDescription className="text-[13px] font-medium text-[#888]">
                Biblioteca Facultad de Ingeniería
              </CardDescription>
            </div>
          </CardHeader>
          <CardContent className="px-10 pb-12 space-y-8">
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email" className="text-[12px] font-bold uppercase tracking-wider text-[#111]">Correo Institucional</Label>
                <Input 
                  id="email" 
                  type="email" 
                  placeholder="ejemplo@fi.uba.ar" 
                  className="h-12 border-gray-200 focus:border-[#1a73e8] focus:ring-[#1a73e8]/20 rounded-lg"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="password" className="text-[12px] font-bold uppercase tracking-wider text-[#111]">Contraseña</Label>
                <Input 
                  id="password" 
                  type="password" 
                  className="h-12 border-gray-200 focus:border-[#1a73e8] focus:ring-[#1a73e8]/20 rounded-lg"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 pt-2">
              <Button 
                onClick={() => handleLogin("student")}
                className="h-14 bg-[#111] hover:bg-[#333] text-white font-bold rounded-xl shadow-lg hover:shadow-black/10 transition-all flex items-center gap-2 border-none"
              >
                <User className="w-4 h-4" /> Soy Alumno
              </Button>
              <Button 
                onClick={() => handleLogin("admin")}
                variant="outline"
                className="h-14 border-[1.5px] border-[#1a73e8] text-[#1a73e8] hover:bg-[#1a73e8]/5 font-bold rounded-xl transition-all flex items-center gap-2"
              >
                <ShieldCheck className="w-4 h-4" /> Administrador
              </Button>
            </div>

            <p className="text-center text-[11px] text-[#aaa] font-medium">
              Al ingresar aceptas los términos y condiciones de la biblioteca.
            </p>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
