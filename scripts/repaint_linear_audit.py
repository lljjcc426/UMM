"""Exact-moment check of arXiv:2302.01217v1 Theorem 8.

This calculates the population least-squares objective written in the paper.
It does not train a diffusion model or reproduce the authors' experiments.
The derivation and scope are documented in the accompanying evidence note.
"""
import json
from math import sqrt
from statistics import mean


def audit():
    # A = (1, 0)^T, z and epsilon standard independent Gaussians,
    # t uniform on {1, 2}; the final time feature has zero optimal coefficient.
    betas = [0.2, 0.5]
    alphas = [1 - b for b in betas]
    bar_prev = [1.0, alphas[0]]
    bars = [p * a for p, a in zip(bar_prev, alphas)]
    # In coordinate 2 the clean data vanish. These are exact population moments.
    variance = mean(1 - b for b in bars)
    cross = mean(sqrt(a) * (1 - p) for a, p in zip(alphas, bar_prev))
    optimum = cross / variance
    published_gamma = mean(1 / (1 - b) for b in bars) * cross
    gradient = 2 * (variance * published_gamma - cross)
    excess_loss = variance * (published_gamma - optimum) ** 2
    return {
        "source": "https://arxiv.org/html/2302.01217v1#S3.SS2.SSS4",
        "scope": "local population-moment audit of Theorem 8 as written; not model reproduction",
        "setting": {"A": [[1], [0]], "beta_0": 0, "betas": betas,
                    "t_uniform": [1, 2], "alpha_bar": bars},
        "coordinate": 2,
        "E_x_squared": variance,
        "E_target_x": cross,
        "least_squares_coefficient": optimum,
        "published_gamma": published_gamma,
        "objective_derivative_at_published_gamma": gradient,
        "excess_population_loss": excess_loss,
        "exact_values": {"optimum": "sqrt(2)/8", "published_gamma": "sqrt(2)/6",
                         "gradient": "sqrt(2)/30", "excess_loss": "1/720"},
        "conclusion": "The stated coefficient is not stationary for the stated unweighted objective in this setting. This does not reject the separate two-state contraction argument."
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
