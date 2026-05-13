import { useNavigate } from "react-router-dom";
import { Languages, Globe, BookMarked } from "lucide-react";

export function CourseTypePage() {
  const navigate = useNavigate();

  const courseTypes = [
    {
      id: "ingles",
      title: "Inglés",
      description: "Cursos de inglés para todos los niveles",
      icon: Languages,
      color: "bg-blue-600 hover:bg-blue-700",
    },
    {
      id: "otros-idiomas",
      title: "Otros Idiomas",
      description: "Francés, alemán, italiano, portugués y más",
      icon: Globe,
      color: "bg-indigo-600 hover:bg-indigo-700",
    },
    {
      id: "comprension-lectora",
      title: "Comprensión Lectora",
      description: "Mejora tus habilidades de lectura y análisis",
      icon: BookMarked,
      color: "bg-purple-600 hover:bg-purple-700",
    },
  ];

  const handleSelect = (type: string) => {
    navigate(`/seleccion-grupo/${type}`);
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-12">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Selecciona el Tipo de Curso
        </h2>
        <p className="text-gray-600">
          Elige el área de estudio de tu interés
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        {courseTypes.map((type) => {
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
