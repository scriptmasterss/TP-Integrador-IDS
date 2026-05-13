import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Checkbox } from "../components/ui/checkbox";
import { Alert, AlertDescription } from "../components/ui/alert";
import { Upload, AlertCircle } from "lucide-react";

export function PaymentPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [confirmEmail, setConfirmEmail] = useState("");
  const [comprobante, setComprobante] = useState<File | null>(null);
  const [requiresCFDI, setRequiresCFDI] = useState(false);

  const selectedCourse = JSON.parse(localStorage.getItem("selectedCourse") || "{}");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (email !== confirmEmail) {
      alert("Los correos electrónicos no coinciden");
      return;
    }

    localStorage.setItem("email", email);

    if (requiresCFDI) {
      navigate("/cfdi");
    } else {
      navigate("/confirmacion");
    }
  };

  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-white rounded-lg shadow-xl p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Información de Pago
        </h2>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <h3 className="font-semibold text-blue-900 mb-2">Curso Seleccionado</h3>
          <p className="text-blue-800">
            <span className="font-medium">{selectedCourse.nivel}</span> - {selectedCourse.horario}
          </p>
          <p className="text-blue-700 text-sm">Profesor: {selectedCourse.profesor}</p>
        </div>

        <Alert className="mb-6">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            Los datos de pago serán enviados al correo electrónico que proporciones a continuación.
            Este correo también será utilizado para tu inicio de sesión una vez completado el pago.
          </AlertDescription>
        </Alert>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <Label htmlFor="email">Correo Electrónico</Label>
            <Input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="mt-1"
              placeholder="correo@ejemplo.com"
            />
            <p className="text-xs text-gray-500 mt-1">
              Recibirás los datos bancarios y tu contraseña temporal en este correo
            </p>
          </div>

          <div>
            <Label htmlFor="confirmEmail">Confirmar Correo Electrónico</Label>
            <Input
              id="confirmEmail"
              type="email"
              value={confirmEmail}
              onChange={(e) => setConfirmEmail(e.target.value)}
              required
              className="mt-1"
              placeholder="correo@ejemplo.com"
            />
          </div>

          <div className="border-t pt-6">
            <h3 className="font-semibold text-gray-900 mb-4">Comprobante de Pago</h3>
            <p className="text-sm text-gray-600 mb-4">
              Una vez que hayas realizado el pago, adjunta tu comprobante aquí:
            </p>

            <div>
              <Label htmlFor="comprobante">Adjuntar Comprobante</Label>
              <div className="mt-1 flex items-center gap-4">
                <Input
                  id="comprobante"
                  type="file"
                  onChange={(e) => setComprobante(e.target.files?.[0] || null)}
                  required
                  accept=".pdf,.jpg,.jpeg,.png"
                  className="flex-1"
                />
                <Upload className="w-5 h-5 text-gray-400" />
              </div>
              <p className="text-xs text-gray-500 mt-1">
                Formatos aceptados: PDF, JPG, PNG (máx. 5MB)
              </p>
            </div>
          </div>

          <div className="border-t pt-6">
            <div className="flex items-center space-x-2">
              <Checkbox
                id="cfdi"
                checked={requiresCFDI}
                onCheckedChange={(checked) => setRequiresCFDI(checked as boolean)}
              />
              <Label
                htmlFor="cfdi"
                className="text-sm font-medium cursor-pointer"
              >
                Solicitar Factura (CFDI)
              </Label>
            </div>
            {requiresCFDI && (
              <p className="text-xs text-gray-500 mt-2 ml-6">
                Se requerirá tu Constancia de Situación Fiscal en el siguiente paso
              </p>
            )}
          </div>

          <div className="flex gap-4">
            <Button type="button" variant="outline" onClick={() => navigate(-1)} className="flex-1">
              Regresar
            </Button>
            <Button type="submit" className="flex-1">
              {requiresCFDI ? "Continuar con CFDI" : "Finalizar Inscripción"}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
