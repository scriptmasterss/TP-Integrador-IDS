import { useNavigate } from "react-router-dom";
import { Button } from "../components/ui/button";
import { CheckCircle, Mail } from "lucide-react";

export function ConfirmationPage() {
  const navigate = useNavigate();
  const email = localStorage.getItem("email") || "";
  const selectedCourse = JSON.parse(localStorage.getItem("selectedCourse") || "{}");

  const handleFinish = () => {
    localStorage.clear();
    navigate("/");
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white rounded-lg shadow-xl p-8 text-center">
        <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <CheckCircle className="w-12 h-12 text-green-600" />
        </div>

        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          ¡Inscripción Completada!
        </h2>

        <p className="text-gray-600 mb-8">
          Tu solicitud de inscripción ha sido procesada exitosamente
        </p>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6 text-left">
          <h3 className="font-semibold text-blue-900 mb-3">Detalles de tu Inscripción</h3>
          <div className="space-y-2 text-blue-800">
            <p>
              <span className="font-medium">Curso:</span> {selectedCourse.nivel}
            </p>
            <p>
              <span className="font-medium">Horario:</span> {selectedCourse.horario}
            </p>
            <p>
              <span className="font-medium">Profesor:</span> {selectedCourse.profesor}
            </p>
          </div>
        </div>

        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 mb-8">
          <div className="flex items-start gap-3">
            <Mail className="w-5 h-5 text-yellow-600 mt-0.5 flex-shrink-0" />
            <div className="text-left">
              <h4 className="font-semibold text-yellow-900 mb-2">
                Revisa tu correo electrónico
              </h4>
              <p className="text-sm text-yellow-800 mb-2">
                Hemos enviado un correo a <span className="font-medium">{email}</span> con:
              </p>
              <ul className="text-sm text-yellow-800 space-y-1">
                <li>• Tu contraseña temporal para iniciar sesión</li>
                <li>• Instrucciones de pago</li>
                <li>• Detalles de tu inscripción</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="space-y-3">
          <p className="text-sm text-gray-600">
            Una vez que tu pago sea verificado, recibirás un correo de confirmación final.
          </p>
          <p className="text-sm text-gray-600">
            Podrás iniciar sesión con tu correo y la contraseña proporcionada.
          </p>
        </div>

        <Button onClick={handleFinish} className="mt-8 w-full">
          Volver a Inicio
        </Button>
      </div>
    </div>
  );
}
