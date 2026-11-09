// csv-schema.data.mts: reads csv-schema.yaml at build time for the CSV Schema page (csv-schema.md).
//
// The YAML is the hand-edited source; this loader only reshapes it for the CsvSchema component and stops the
// build on a broken reference (a link to an undocumented column, a file the layout forgets). That the YAML
// matches the columns eic2ai writes is checked in the eic2ai repository (tests/check_schema.py).
import fs from "node:fs";
import { parse } from "yaml";

export interface SchemaColumn {
    name: string;
    text: string;          // the description without its trailing [unit]
    unit: string;          // the trailing [unit], or ""
    key: boolean;          // part of the columns that identify one row
    linkFile: string;      // the file this column points into, or ""
    linkColumn: string;    // the column it points at in that file, or ""
    group: string;         // the longest `prefixes` entry the name starts with, or ""
}

export interface SchemaFile {
    name: string;
    row: string;           // what one row is
    needs: string;         // which eic2ai inputs the file needs
    keys: string[];
    prefixes: Record<string, string>;
    columns: SchemaColumn[];
}

export interface Schema {
    layout: Record<string, string[]>;   // lane → file names, top to bottom
    laneTitles: Record<string, string>;
    files: Record<string, SchemaFile>;
    nColumns: number;
}

export declare const data: Schema;

const UNIT = /^(.*?)\s*\[([^\]]+)\]\s*$/;

export default {
    watch: ["./csv-schema.yaml"],
    load([path]: string[]): Schema {
        const source = parse(fs.readFileSync(path, "utf-8"));
        const problems: string[] = [];
        const files: Record<string, SchemaFile> = {};

        for (const [name, entry] of Object.entries<any>(source.files ?? {})) {
            const keys: string[] = entry.keys ?? [];
            const prefixes: Record<string, string> = entry.prefixes ?? {};
            const links: Record<string, string> = entry.links ?? {};
            const byLength = Object.keys(prefixes).sort((a, b) => b.length - a.length);
            const columns = Object.entries<any>(entry.columns ?? {}).map(([column, description]) => {
                const text = String(description ?? "");
                const unit = text.match(UNIT);
                const [linkFile, linkColumn] = (links[column] ?? "").split(".");
                return {
                    name: column,
                    text: unit ? unit[1] : text,
                    unit: unit ? unit[2] : "",
                    key: keys.includes(column),
                    linkFile: linkFile ?? "",
                    linkColumn: linkColumn ?? "",
                    group: byLength.find((prefix) => column.startsWith(prefix + "_")) ?? "",
                };
            });
            for (const column of [...keys, ...Object.keys(links)]) {
                if (!columns.some((c) => c.name === column)) problems.push(`${name}: ${column} is not a column`);
            }
            files[name] = { name, row: String(entry.row ?? ""), needs: String(entry.needs ?? ""), keys, prefixes, columns };
        }

        for (const file of Object.values(files)) {
            for (const column of file.columns.filter((c) => c.linkFile)) {
                const target = files[column.linkFile];
                if (!target || !target.columns.some((c) => c.name === column.linkColumn)) {
                    problems.push(`${file.name}: link ${column.name} → ${column.linkFile}.${column.linkColumn} names no documented column`);
                }
            }
        }
        const layout: Record<string, string[]> = source.layout ?? {};
        const placed = Object.values(layout).flat();
        for (const name of Object.keys(files)) {
            if (placed.filter((p) => p === name).length !== 1) problems.push(`layout: place ${name} exactly once`);
        }
        for (const name of placed) {
            if (!files[name]) problems.push(`layout: ${name} is not a documented file`);
        }
        if (problems.length) throw new Error(`csv-schema.yaml:\n  ${problems.join("\n  ")}`);

        const nColumns = Object.values(files).reduce((sum, file) => sum + file.columns.length, 0);
        return { layout, laneTitles: source.lane_titles ?? {}, files, nColumns };
    },
};
