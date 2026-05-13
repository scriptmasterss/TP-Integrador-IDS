import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Button } from "../components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "../components/ui/table";
import { Badge } from "../components/ui/badge";
import { Check } from "lucide-react";

const coursesData = {
  ingles: [
    { id: 1, nivel: "Básico 1", horario: "Lun-Mie 8:00-10:00", profesor: "Dr. García López", cupo: 5, total: 25 },
    { id: 2, nivel: "Básico 2", horario: "Mar-Jue 10:00-12:00", profesor: "Mtra. Martínez Silva", cupo: 12, total: 25 },
    { id: 3, nivel: "Intermedio 1", horario: "Lun-Mie 14:00-16:00", profesor: "Dr. Rodríguez Pérez", cupo: 8, total: 25 },
    { id: 4, nivel: "Intermedio 2", horario: "Mar-Jue 16:00-18:00", profesor: "Mtra. Hernández Cruz", cupo: 0, total: 25 },
    { id: 5, nivel: "Avanzado 1", horario: "Lun-Mie 18:00-20:00", profesor: "Dr. López Ramírez", cupo: 15, total: 25 },
  ],
  "otros-idiomas": [
    { id: 6, nivel: "Francés Básico", horario: "Mar-Jue 9:00-11:00", profesor: "Mtra. Dubois", cupo: 10, total: 20 },
    { id: 7, nivel: "Alemán Básico", horario: "Lun-Mie 11:00-13:00", profesor: "Dr. Müller", cupo: 7, total: 20 },
    { id: 8, nivel: "Italiano Básico", horario: "Mar-Jue 13:00-15:00", profesor: "Mtra. Rossi", cupo: 3, total: 20 },
    { id: 9, nivel: "Portugués Básico", horario: "Lun-Mie 15:00-17:00", profesor: "Dr. Silva", cupo: 12, total: 20 },
  ],
  "comprension-lectora": [
    { id: 10, nivel: "Nivel 1", horario: "Lun-Mie 10:00-12:00", profesor: "Dr. Sánchez Torres", cupo: 8, total: 30 },
    { id: 11, nivel: "Nivel 2", horario: "Mar-Jue 12:00-14:00", profesor: "Mtra. Flores Vega", cupo: 5, total: 30 },
    { id: 12, nivel: "Nivel 3", horario: "Lun-Mie 16:00-18:00", profesor: "Dr. Castro Ruiz", cupo: 18, total: 30 },
  ],
};

export function GroupSelectionPage() {
  const { courseType } = useParams<{ courseType: string }>();
  const navigate = useNavigate();
  const [selectedGroup, setSelectedGroup] = useState<number | null>(null);

  const courses = coursesData[courseType as keyof typeof coursesData] || [];

  const getCourseTitle = () => {
    switch (courseType) {
      case "ingles":
        return "Inglés";
      case "otros-idiomas":
        return "Otros Idiomas";
      case "comprension-lectora":
        return "Comprensión Lectora";
      default:
        return "Cursos";
    }
  };

  const handleContinue = () => {
    if (selectedGroup) {
      const selected = courses.find((c) => c.id === selectedGroup);
      localStorage.setItem("selectedCourse", JSON.stringify(selected));
      navigate("/pago");
    }
  };

  return (
    <div className="max-w-5xl mx-auto">
      <div className="bg-white rounded-lg shadow-xl p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Disponibilidad de Grupos - {getCourseTitle()}
        </h2>
        <p className="text-gray-600 mb-6">
          Selecciona el grupo que mejor se adapte a tu horario
        </p>

        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-12"></TableHead>
                <TableHead>Nivel/Curso</TableHead>
                <TableHead>Horario</TableHead>
                <TableHead>Profesor</TableHead>
                <TableHead>Disponibilidad</TableHead>
                <TableHead>Estado</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {courses.map((course) => {
                const isSelected = selectedGroup === course.id;
                const isAvailable = course.cupo > 0;

                return (
                  <TableRow
                    key={course.id}
                    className={`cursor-pointer ${
                      isSelected ? "bg-blue-50" : isAvailable ? "hover:bg-gray-50" : "opacity-50"
                    }`}
                    onClick={() => isAvailable && setSelectedGroup(course.id)}
                  >
                    <TableCell>
                      <div
                        className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                          isSelected
                            ? "border-blue-600 bg-blue-600"
                            : "border-gray-300"
                        }`}
                      >
                        {isSelected && <Check className="w-3 h-3 text-white" />}
                      </div>
                    </TableCell>
                    <TableCell className="font-medium">{course.nivel}</TableCell>
                    <TableCell>{course.horario}</TableCell>
                    <TableCell>{course.profesor}</TableCell>
                    <TableCell>
                      {course.cupo} de {course.total} lugares
                    </TableCell>
                    <TableCell>
                      {isAvailable ? (
                        <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                          Disponible
                        </Badge>
                      ) : (
                        <Badge variant="outline" className="bg-red-50 text-red-700 border-red-200">
                          Lleno
                        </Badge>
                      )}
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </div>

        <div className="mt-8 flex justify-between items-center">
          <Button variant="outline" onClick={() => navigate("/tipo-curso")}>
            Regresar
          </Button>
          <Button onClick={handleContinue} disabled={!selectedGroup}>
            Continuar con Inscripción
          </Button>
        </div>
      </div>
    </div>
  );
}
