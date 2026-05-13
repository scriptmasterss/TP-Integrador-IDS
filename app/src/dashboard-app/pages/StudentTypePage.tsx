import { useNavigate } from "react-router-dom";
import { Button } from "../components/ui/button";
import { GraduationCap, Users, Globe } from "lucide-react";

export function StudentTypePage() {
  const navigate = useNavigate();

  const studentTypes = [
    {
      id: "fca",
      title: "Comunidad FCA",
      description: "Estudiantes y personal de la Facultad de Contaduría y Administración",
      icon: GraduationCap,
      color: "bg-blue-600 hover:bg-blue-700",
    },
    {
      id: "unam",
      title: "Comunidad UNAM",
      description: "Estudiantes y personal de otras facultades de la UNAM",
      icon: Users,
      color: "bg-indigo-600 hover:bg-indigo-700",
    },
    {
      id: "general",
      title: "Público General",
      description: "Personas externas a la UNAM",
      icon: Globe,
      color: "bg-purple-600 hover:bg-purple-700",
    },
  ];

  const handleSelect = (type: string) => {
    localStorage.setItem("studentType", type);
    navigate("/datos-personales");
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-12">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Selecciona tu Tipo de Alumno
        </h2>
        <p className="text-gray-600">
          Elige la categoría que mejor te describa para continuar con el registro
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        {studentTypes.map((type) => {
          const Icon = type.icon;
          return (
            <button
              key={type.id}
              onClick={() => handleSelect(type.id)}
              className="bg-white rounded-lg shadow-lg p-8 hover:shadow-xl transition-shadow text-center group"
            >
              <div className={`${type.color} w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 transition-transform group-hover:scale-110`}>
                <Icon className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                {type.title}
              </h3>
              <p className="text-gray-600 text-sm">
                {type.description}
              </p>
            </button>
          );
        })}
      </div>
    </div>
  );
}
