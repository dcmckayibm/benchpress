"""Test summit benchmarks"""

from qiskit import QuantumCircuit
from qiskit.circuit.library import EfficientSU2

from qiskit_transpiler_service.transpiler_service import TranspilerService

from benchpress.config import Configuration
from benchpress.qiskit_gym.circuits import bv_all_ones

from benchpress.workouts.validation import benchpress_test_validation
from benchpress.workouts.device_transpile import WorkoutDeviceTranspile100Q
from benchpress.qiskit_gym.circuits import trivial_bvlike_circuit

BACKEND = Configuration.backend()
OPTIMIZATION_LEVEL = Configuration.options["qiskit"]["optimization_level"]

TRANS_SERVICE = TranspilerService(
    coupling_map=list(BACKEND.coupling_map.get_edges()),
    qiskit_transpile_options = {'basis_gates': BACKEND.operation_names},
    ai=True,
    optimization_level=OPTIMIZATION_LEVEL,
)


@benchpress_test_validation
class TestWorkoutDeviceTranspile100Q(WorkoutDeviceTranspile100Q):
    def test_QFT_100_transpile(self, benchmark):
        """Compile 100Q QFT circuit against target backend"""
        circuit = QuantumCircuit.from_qasm_file(
            Configuration.get_qasm_dir("qft") + "qft_N100.qasm"
        )
        @benchmark
        def result():
            trans_qc = TRANS_SERVICE.run(circuit)
            return trans_qc

        benchmark.extra_info["gate_count_2q"] = result.count_ops().get("cz", 0)
        benchmark.extra_info["depth_2q"] = result.depth(
            filter_function=lambda x: x.operation.name == "cz"
        )
        assert result

    def test_QV_100_transpile(self, benchmark):
        """Compile 10Q QV circuit against target backend"""
        circuit = QuantumCircuit.from_qasm_file(
            Configuration.get_qasm_dir("qv") + "qv_N100_12345.qasm"
        )

        @benchmark
        def result():
            trans_qc = TRANS_SERVICE.run(circuit)
            return trans_qc

        benchmark.extra_info["gate_count_2q"] = result.count_ops().get("cz", 0)
        benchmark.extra_info["depth_2q"] = result.depth(
            filter_function=lambda x: x.operation.name == "cz"
        )
        assert result

    def test_circSU2_100_transpile(self, benchmark):
        """Compile 100Q circSU2 circuit against target backend"""
        circuit = EfficientSU2(100, reps=3, entanglement="circular")

        @benchmark
        def result():
            trans_qc = TRANS_SERVICE.run(circuit)
            return trans_qc

        benchmark.extra_info["gate_count_2q"] = result.count_ops().get("cz", 0)
        benchmark.extra_info["depth_2q"] = result.depth(
            filter_function=lambda x: x.operation.name == "cz"
        )
        assert result

    def test_BV_100_transpile(self, benchmark):
        """Compile 100Q BV circuit against target backend"""
        circuit = bv_all_ones(100)

        @benchmark
        def result():
            trans_qc = TRANS_SERVICE.run(circuit)
            return trans_qc

        benchmark.extra_info["gate_count_2q"] = result.count_ops().get("cz", 0)
        benchmark.extra_info["depth_2q"] = result.depth(
            filter_function=lambda x: x.operation.name == "cz"
        )
        assert result

    def test_square_heisenberg_100_transpile(self, benchmark):
        """Compile 100Q square-Heisenberg circuit against target backend"""
        circuit = QuantumCircuit.from_qasm_file(
            Configuration.get_qasm_dir("square-heisenberg")
            + "square_heisenberg_N100.qasm"
        )

        @benchmark
        def result():
            trans_qc = TRANS_SERVICE.run(circuit)
            return trans_qc

        benchmark.extra_info["gate_count_2q"] = result.count_ops().get("cz", 0)
        benchmark.extra_info["depth_2q"] = result.depth(
            filter_function=lambda x: x.operation.name == "cz"
        )
        assert result

    def test_QAOA_100_transpile(self, benchmark):
        """Compile 100Q QAOA circuit against target backend"""
        circuit = QuantumCircuit.from_qasm_file(
            Configuration.get_qasm_dir("qaoa") + "qaoa_barabasi_albert_N100_3reps.qasm"
        )

        @benchmark
        def result():
            trans_qc = TRANS_SERVICE.run(circuit)
            return trans_qc

        benchmark.extra_info["gate_count_2q"] = result.count_ops().get("cz", 0)
        benchmark.extra_info["depth_2q"] = result.depth(
            filter_function=lambda x: x.operation.name == "cz"
        )
        assert result

    def test_BVlike_simplification_transpile(self, benchmark):
        """Transpile a BV-like circuit that should collapse down
        into a single X and Z gate on a target device
        """
        circuit = trivial_bvlike_circuit(100)

        @benchmark
        def result():
            trans_qc = TRANS_SERVICE.run(circuit)
            return trans_qc

        benchmark.extra_info["gate_count_2q"] = result.count_ops().get("cz", 0)
        benchmark.extra_info["depth_2q"] = result.depth(
            filter_function=lambda x: x.operation.name == "cz"
        )
        assert result