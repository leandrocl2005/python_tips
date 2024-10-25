aluno = {
    "name": "Frederico Martins",
    "completou_ensino_medio": True,
    "disciplinas_obrigatorias": {
        "fundamentos": {"carga_horaria": 60, "aprovado": True, "nota": 9.5},
        "geometria_analitica": {"carga_horaria": 60, "aprovado": True, "nota": 9.7},
        "algebra_linear": {"carga_horaria": 60, "aprovado": True, "nota": 9.5},
    },
    "disciplinas_eletivas": {
        "ciencia_dados": {"carga_horaria": 60, "aprovado": True, "nota": 7.8},
        "empreendedorismo": {"carga_horaria": 60, "aprovado": False, "nota": 4.2},
    },
    "complementares": [
        {
            "title": "previsão preço bitcoin",
            "carga_horaria": 240,
            "max_carga_horaria": 120,
            "concluido": True,
            "tipo": "projeto_ic",
        },
        {
            "title": "otimização de sistemas de irrigação",
            "carga_horaria": 240,
            "max_carga_horaria": 0,
            "concluido": True,
            "tipo": "projeto_ic",
        },
        {
            "title": "forró",
            "carga_horaria": 120,
            "max_carga_horaria": 120,
            "concluido": True,
            "tipo": "projeto_extensao",
        },
        {
            "title": "Mãos amigas",
            "carga_horaria": 120,
            "max_carga_horaria": 120,
            "concluido": False,
        },
        {
            "title": "Rondom",
            "carga_horaria": 240,
            "max_carga_horaria": 120,
            "concluido": True,
        },
    ],
}


def compute_horas_obrigatorias(
    algebra_linear, geometria_analitica, fundamentos, **kwargs
):
    horas_obrigatorias = 0
    if algebra_linear["aprovado"]:
        horas_obrigatorias += algebra_linear["carga_horaria"]
    if geometria_analitica["aprovado"]:
        horas_obrigatorias += geometria_analitica["carga_horaria"]
    if fundamentos["aprovado"]:
        horas_obrigatorias += fundamentos["carga_horaria"]
    return horas_obrigatorias


def compute_horas_eletivas(disciplinas_eletivas, **kwargs):
    carga_horaria_eletivas = 0
    for disciplina in disciplinas_eletivas:
        if disciplinas_eletivas[disciplina]["aprovado"]:
            carga_horaria_eletivas += disciplinas_eletivas[disciplina]["carga_horaria"]
    return carga_horaria_eletivas


def compute_cr(
    algebra_linear, geometria_analitica, fundamentos, disciplinas_eletivas, **kwargs
):
    cr = 0
    if algebra_linear["aprovado"]:
        cr += algebra_linear["nota"]
    if geometria_analitica["aprovado"]:
        cr += geometria_analitica["nota"]
    if fundamentos["aprovado"]:
        cr += fundamentos["nota"]
    count = 0
    for disciplina_eletiva in disciplinas_eletivas:
        count += 1
        if disciplinas_eletivas[disciplina_eletiva]["aprovado"]:
            cr += disciplinas_eletivas[disciplina_eletiva]["nota"]
    cr = cr / (3 + count)
    return cr


def validate_obrigatorias(algebra_linear, geometria_analitica, fundamentos, **kwargs):
    if not algebra_linear["aprovado"]:
        raise ValueError("aluno não foi aprovado em álgebra linear")
    if not geometria_analitica["aprovado"]:
        raise ValueError("aluno não foi aprovado em álgebra linear")
    if not fundamentos["aprovado"]:
        raise ValueError("aluno não foi aprovado em álgebra linear")


def validate_eletivas(
    algebra_linear, geometria_analitica, fundamentos, disciplinas_eletivas, **kwargs
):
    horas_obrigatorias = compute_horas_obrigatorias(
        algebra_linear, geometria_analitica, fundamentos
    )
    if horas_obrigatorias < 180:
        raise ValueError("Aluno não tem horas obrigatórias para validar eletivas")
    carga_horaria_eletivas = compute_horas_eletivas(disciplinas_eletivas)
    if carga_horaria_eletivas < 60:
        raise ValueError("Aluno não completou as eletivas.")


def validate_complementares(
    algebra_linear, geometria_analitica, fundamentos, complementares, **kwargs
):
    horas_obrigatorias = compute_horas_obrigatorias(
        algebra_linear, geometria_analitica, fundamentos
    )
    if horas_obrigatorias < 120:
        raise ValueError("Aluno não tem horas obrigatórias para validar complementares")
    carga_horaria_complementares = 0
    for complementar in complementares:
        if complementar["concluido"]:
            carga_horaria_complementares += complementar["max_carga_horaria"]
    if carga_horaria_complementares < 240:
        raise ValueError("Aluno não completou as complementares.")


def validate_ensino_medio(completou_ensino_medio, **kwargs):
    if not completou_ensino_medio:
        raise ValueError("Aluno não completou o ensino médio")


def gerar_certificado_com_cr_e_ch(aluno):

    data = {
        "name": aluno["name"],
        "geometria_analitica": aluno["disciplinas_obrigatorias"]["geometria_analitica"],
        "algebra_linear": aluno["disciplinas_obrigatorias"]["algebra_linear"],
        "fundamentos": aluno["disciplinas_obrigatorias"]["fundamentos"],
        "disciplinas_eletivas": aluno["disciplinas_eletivas"],
        "complementares": aluno["complementares"],
        "completou_ensino_medio": aluno["completou_ensino_medio"],
    }

    # aluno deve ter cursado todas disciplinas obrigatórias (geometria, algebra e fundamentos)
    validate_obrigatorias(**data)

    # aluno deve ter cursado 180 disciplinas obrigatórias para validar eletivas *** DRY
    # aluno deve ter cursado 60 horas de disciplinas eletivas
    validate_eletivas(**data)

    # alunos deve ter completado 240 horas complementares
    # aluno deve ter cursado 120 horas de disciplinas obrigatórias para validar complementares *** DRY
    validate_complementares(**data)

    # aluno deve ter concluído o médio
    validate_ensino_medio(**data)

    cr = compute_cr(**data)
    ch_eletivas = compute_horas_eletivas(**data)
    ch_obrigatorias = compute_horas_obrigatorias(**data)
    ch_total = ch_eletivas + ch_obrigatorias

    return f"{data['name']} completou a graduação com CH de {ch_total} e CR de {cr}"


print(gerar_certificado_com_cr_e_ch(aluno))
