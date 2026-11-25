# 이산위상 연구실 (Discrete Topology Lab)

이산위상을 기초 공리부터 범주론의 보편 대상까지 따라가는 연구실 해설 시리즈입니다.

글 · 안상선 ((주)M-Robo 대표)

## 구성 — 원본 장표 20장 (`slides/`)

| 장 | 제목 | 묶음 |
|---|---|---|
| 01 | The Architecture of Discrete Topology | 개요 |
| 02 | Foundations of Topological Spaces | 공간 분류 |
| 03 | The Discrete Topology and Maximal Structural Distinction | 공간 분류 |
| 04 | Compactness and Topological Finiteness | 공간 분류 |
| 05 | Connectedness and Topological Separation | 공간 분류 |
| 06 | Alexandroff Spaces and Poset Equivalence | 공간 분류 |
| 07 | Digital Topology: The Khalimsky and Rosenfeld Models | 공간 분류 |
| 08 | Semi-Topological and Pre-Topological Spaces | 공간 분류 |
| 09 | Discrete Groups and Continuous Actions | 군 작용 |
| 10 | The Hierarchy of Properly Discontinuous Actions | 군 작용 |
| 11 | Fundamental Sets and Dirichlet Domains | 군 작용 |
| 12 | Covering Spaces and Path Lifts | 군 작용 |
| 13 | Universal Covers & The Topological Galois Correspondence | 보편 대상 |
| 14 | The Stone-Čech Compactification (βX) | 보편 대상 |
| 15 | Ultrafilters as Points at Infinity | 보편 대상 |
| 16 | Extremally Disconnected Spaces | 보편 대상 |
| 17 | Profinite Spaces and Groups | 보편 대상 |
| 18 | Lattices and Discrete Subgroups of Lie Groups | 군 작용 |
| 19 | The Categorical Architecture of Discrete Topology | 보편 대상 |
| 20 | Conclusion: The Pervasive Utility of Discrete Constructs | 결론 |

## 해설로 옮길 때 고칠 점

**내용 수정**
- 19장: Disc 함자는 집합에 *이산위상*을 주는 함자다 (항등 사상만 있는 범주는 이산 범주). Hom_Set 화살표 방향, "topology topology" 중복도 고친다.
- 06장: 열린집합은 각 점의 가장 작은 열린 근방들의 (임의) 합집합이다. 순서 집합과 대응하는 것은 T0 알렉산드로프 공간이고, 일반 알렉산드로프 공간은 준순서와 대응한다.
- 05장: 아래 그림 두 개가 서로 바뀌어 있다.
- 13장: 2행은 동형이 아니라 유비 관계다. "X̃~" 오타.
- 04장: ℝⁿ 예시는 하이네-보렐(유계 닫힌집합)이라고 밝힌다. ℝⁿ 자체는 콤팩트가 아니다.

**다듬기**
- 02장 기저 조건: x ∈ B₁∩B₂이면 x ∈ B₃ ⊆ B₁∩B₂인 B₃가 있다.
- 08장 반위상 정의의 출처 명시 (알렉산드로프 공간 정의와 겹침).
- 10장 중복 문장, 끊긴 문장.
- 14장 그림 라벨 "disconnects", 20장 그림 라벨 정리.
- 17장: 사유한 군 내용 보강, 호환 조건은 π_ij(x_i) = x_j로 표기.

## 표지

`cover/cover_prompt.md` — 픽셀 열지도와 매끈한 유선으로 이산과 연속을 대비한 16비트 픽셀아트 표지 지시문.
