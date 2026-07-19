from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)
from time import perf_counter
from typing import List
import traceback

from app.moderation.config.detector_registry import (
    get_registered_detectors,
)
from app.moderation.config.moderation_settings import (
    DETECTOR_TIMEOUT,
    IGNORE_DETECTOR_ERRORS,
    MAX_WORKERS,
    SHOW_DETECTOR_TIME,
    SHOW_ENGINE_TIME,
)
from app.moderation.detectors.base import BaseDetector
from app.moderation.policies.policy_engine import PolicyEngine
from app.moderation.schemas.moderation_result import (
    ModerationResult,
)


class ModerationEngine:
    """
    Runs all moderation detectors in parallel.
    """

    def __init__(self):

        self.policy = PolicyEngine()
        self.detectors = get_registered_detectors()

    def register(
        self,
        detector: BaseDetector,
    ):
        self.detectors.append(detector)

    def _run_detector(
        self,
        detector: BaseDetector,
        text: str,
    ) -> ModerationResult:

        start = perf_counter()

        try:

            result = detector.analyze(text)

        except Exception as e:

            print("\n" + "=" * 80)
            print(f"❌ ERROR inside detector: {detector.name}")
            traceback.print_exc()
            print("=" * 80 + "\n")

            if not IGNORE_DETECTOR_ERRORS:
                raise

            result = ModerationResult(
                category=detector.name,
                detected=False,
                severity="error",
                confidence=0,
                blocked=False,
                reason=str(e),
            )

        end = perf_counter()

        if SHOW_DETECTOR_TIME:
            print(
                f"{detector.name:<20}"
                f"{(end - start) * 1000:.2f} ms"
            )

        return result

    def analyze(
        self,
        text: str,
    ):

        engine_start = perf_counter()

        results: List[ModerationResult] = []

        with ThreadPoolExecutor(
            max_workers=MAX_WORKERS,
        ) as executor:

            futures = {
                executor.submit(
                    self._run_detector,
                    detector,
                    text,
                ): detector
                for detector in self.detectors
            }

            for future in as_completed(futures):
                detector = futures[future]
                try:

                    result = future.result(
                        timeout=DETECTOR_TIMEOUT,
                    )

                    results.append(result)

                except TimeoutError:

                    print(f"⚠ {detector.name} timed out.")

                    results.append(
                        ModerationResult(
                            category=detector.name,
                            detected=False,
                            severity="error",
                            confidence=0,
                            blocked=False,
                            reason="Detector timeout",
                        )
                    )

                except Exception as e:

                    print("\n" + "=" * 80)
                    print(f"❌ FUTURE ERROR: {detector.name}")
                    traceback.print_exc()
                    print("=" * 80 + "\n")

                    results.append(
                        ModerationResult(
                            category=detector.name,
                            detected=False,
                            severity="error",
                            confidence=0,
                            blocked=False,
                            reason=str(e),
                        )
                    )

        response = self.policy.evaluate(results)

        engine_end = perf_counter()

        if SHOW_ENGINE_TIME:
            print("\n======================================")
            print(
                f"Total Moderation Time : {(engine_end - engine_start) * 1000:.2f} ms"
            )
            print("======================================\n")

        return response