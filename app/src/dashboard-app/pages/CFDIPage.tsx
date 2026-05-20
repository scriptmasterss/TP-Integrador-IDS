import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Upload } from "lucide-react";

export function CFDIPage() {
  const navigate = useNavigate();
  const [constancia, setConstancia] = useState<File | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    navigate("/confirmacion");
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white rounded-lg shadow-xl p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Solicitud de Factura (CFDI)
        </h2>

        <p className="text-gray-600 mb-6">
          Para poder emitir tu factura, necesitamos que adjuntes tu Constancia de Situación Fiscal
          actualizada. Puedes obtenerla desde el portal del SAT.
        </p>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <Label htmlFor="constancia">Constancia de Situación Fiscal</Label>
            <div className="mt-1 flex items-center gap-4">
              <Input
                id="constancia"
                type="file"
                onChange={(e) => setConstancia(e.target.files?.[0] || null)}
                required
                accept=".pdf"
                className="flex-1"
              />
              <Upload className="w-5 h-5 text-gray-400" />
            </div>
            <p className="text-xs text-gray-500 mt-1">
              Formato aceptado: PDF (máx. 5MB)
            </p>
          </div>

          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <h4 className="font-semibold text-yellow-900 mb-2">Importante</h4>
            <ul className="text-sm text-yellow-800 space-y-1">
              <li>• La constancia debe estar vigente (no mayor a 30 días)</li>
              <li>• Debe coincidir con el nombre del solicitante</li>
              <li>• La factura será enviada al correo proporcionado anteriormente</li>
            </ul>
          </div>

          <div className="flex gap-4">
            <Button type="button" variant="outline" onClick={() => navigate(-1)} className="flex-1">
              Regresar
            </Button>
            <Button type="submit" className="flex-1">
              Finalizar Inscripción
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
