import { useNavigate } from "react-router-dom";
import { BookOpen, FileText, Trophy } from "lucide-react";

export function ProcedureTypePage() {
  const navigate = useNavigate();

  const procedures = [
    {
      id: "cursos",
      title: "Inscripción a Cursos",
      description: "Inscríbete a cursos de idiomas y comprensión lectora",
      icon: BookOpen,
      color: "bg-blue-600",
      enabled: true,
    },
    {
      id: "examenes",
      title: "Exámenes",
      description: "Registro para exámenes de certificación y diagnóstico",
      icon: FileText,
      color: "bg-gray-400",
      enabled: false,
    },
    {
      id: "extracurriculares",
      title: "Actividades Extracurriculares",
      description: "Inscripción a talleres y actividades complementarias",
      icon: Trophy,
      color: "bg-gray-400",
      enabled: false,
    },
  ];

  const handleSelect = (id: string) => {
    if (id === "cursos") {
      navigate("/tipo-curso");
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-12">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Selecciona el Tipo de Trámite
        </h2>
        <p className="text-gray-600">
          Elige el servicio al que deseas inscribirte
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        {procedures.map((procedure) => {
          const Icon = procedure.icon;
          return (
            <button
              key={procedure.id}
              onClick={() => handleSelect(procedure.id)}
              disabled={!procedure.enabled}
              className={`bg-white rounded-lg shadow-lg p-8 text-center transition-all ${
                procedure.enabled
                  ? "hover:shadow-xl cursor-pointer group"
                  : "opacity-50 cursor-not-allowed"
              }`}
            >
              <div className={`${procedure.color} w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 ${
                procedure.enabled ? "group-hover:scale-110 transition-transform" : ""
              }`}>
                <Icon className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                {procedure.title}
              </h3>
              <p className="text-gray-600 text-sm">
                {procedure.description}
              </p>
              {!procedure.enabled && (
                <p className="text-xs text-gray-500 mt-3 italic">
                  Próximamente disponible
                </p>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}
