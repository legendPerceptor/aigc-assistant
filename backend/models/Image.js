const { DataTypes } = require('sequelize');

const Image = (sequelize) => {
  return sequelize.define('Image', {
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true,
    },
    filename: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    path: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    score: {
      type: DataTypes.INTEGER,
      allowNull: true,
      validate: {
        min: 0,
        max: 10,
      },
    },
    description: {
      type: DataTypes.TEXT,
      allowNull: true,
      comment: 'AI生成的图片描述',
    },
    embedding: {
      type: DataTypes.TEXT,
      allowNull: true,
      comment: '图片嵌入向量(JSON格式)',
      get() {
        const value = this.getDataValue('embedding');
        return value ? JSON.parse(value) : null;
      },
      set(value) {
        this.setDataValue('embedding', value ? JSON.stringify(value) : null);
      },
    },
    embeddingModel: {
      type: DataTypes.STRING,
      allowNull: true,
      comment: '生成嵌入的模型名称',
    },
    analyzedAt: {
      type: DataTypes.DATE,
      allowNull: true,
      comment: 'AI分析时间',
    },
    createdAt: {
      type: DataTypes.DATE,
      defaultValue: DataTypes.NOW,
    },
  });
};

module.exports = Image;
