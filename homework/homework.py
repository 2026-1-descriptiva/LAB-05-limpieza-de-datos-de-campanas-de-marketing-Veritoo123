"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel

import zipfile
import os
import pandas as pd

def clean_campaign_data():
    input_path = "files/input/"
    output_path = "files/output/"

    dataframe = read_zip_and_concat(input_path)

    # client.csv
    client_df = dataframe[
        [
            "client_id",
            "age",
            "job",
            "marital",
            "education",
            "credit_default",
            "mortgage",
        ]
    ].copy()

    client_df["job"] = (
        client_df["job"]
        .str.replace(".", "", regex=False)
        .str.replace("-", "_", regex=False)
    )

    client_df["education"] = (
        client_df["education"]
        .str.replace(".", "_", regex=False)
        .replace("unknown", pd.NA)
    )

    client_df["credit_default"] = (
        client_df["credit_default"]
        .eq("yes")
        .astype(int)
    )

    client_df["mortgage"] = (
        client_df["mortgage"]
        .eq("yes")
        .astype(int)
    )

    save_csv_in_directory(client_df, output_path, "client.csv")

    # campaign.csv
    campaign_df = dataframe[
        [
            "client_id",
            "number_contacts",
            "contact_duration",
            "previous_campaign_contacts",
            "previous_outcome",
            "campaign_outcome",
            "day",
            "month",
        ]
    ].copy()

    campaign_df["previous_outcome"] = (
        campaign_df["previous_outcome"]
        .eq("success")
        .astype(int)
    )

    campaign_df["campaign_outcome"] = (
        campaign_df["campaign_outcome"]
        .eq("yes")
        .astype(int)
    )

    campaign_df["last_contact_date"] = pd.to_datetime(
        campaign_df["day"].astype(str)
        + "-"
        + campaign_df["month"]
        + "-2022",
        format="%d-%b-%Y",
    ).dt.strftime("%Y-%m-%d")

    campaign_df = campaign_df.drop(columns=["day", "month"])

    save_csv_in_directory(
        campaign_df,
        output_path,
        "campaign.csv",
    )

    # economics.csv
    economics_df = dataframe[
        [
            "client_id",
            "cons_price_idx",
            "euribor_three_months",
        ]
    ].copy()

    save_csv_in_directory(
        economics_df,
        output_path,
        "economics.csv",
    )

    print("La operación fue un éxito.")


def read_zip_and_concat(input_path):
    if not os.path.isdir(input_path):
        raise ValueError(
            f"El directorio {input_path} no existe."
        )

    all_data = []

    for zip_name in os.listdir(input_path):

        if not zip_name.endswith(".zip"):
            continue

        zip_path = os.path.join(
            input_path,
            zip_name,
        )

        with zipfile.ZipFile(zip_path, "r") as zip_file:

            csv_files = [
                name
                for name in zip_file.namelist()
                if name.endswith(".csv")
            ]

            if not csv_files:
                continue

            for csv_file in csv_files:

                with zip_file.open(csv_file) as file:

                    df = pd.read_csv(file)

                    all_data.append(df)

    return pd.concat(
        all_data,
        ignore_index=True,
    )


def save_csv_in_directory(
    dataframe,
    output_path,
    filename,
):
    os.makedirs(
        output_path,
        exist_ok=True,
    )

    output_file = os.path.join(
        output_path,
        filename,
    )

    dataframe.to_csv(
        output_file,
        index=False,
    )


if __name__ == "__main__":
    clean_campaign_data()
    
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """

