"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
const mongoose_1 = __importStar(require("mongoose"));
// Define the filterSchema
const filterSchema = new mongoose_1.Schema({
    field: { type: String, required: true },
    options: { type: String, required: true },
});
// Define the main survey schema
const surveySchema = new mongoose_1.Schema({
    title: { type: String, required: true },
    description: { type: String, required: true },
    category: { type: String, required: true },
    filters: { type: [filterSchema], required: false },
    sections: [
        {
            sectionTitle: { type: String, required: true },
            questions: [
                {
                    questionText: { type: String, required: true },
                    choices: { type: [String], required: true },
                },
            ],
        },
    ],
    releaseDate: { type: Date, required: true },
    surveyId: { type: String, unique: true, required: true },
});
const SurveyModel = mongoose_1.default.model('Survey', surveySchema);
exports.default = SurveyModel;
