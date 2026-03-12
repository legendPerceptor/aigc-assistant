const { DataTypes } = require('sequelize');

const Image = (sequelize, dbType = 'sqlite') => {
  const isPostgres = dbType === 'postgres';

  const schema = {
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
  };

  if (isPostgres) {
    schema.embedding = {
      type: DataTypes.TEXT,
      allowNull: true,
      comment: '图片嵌入向量(vector类型或JSON格式)',
    };
    schema.embeddingVector = {
      type: DataTypes.TEXT,
      allowNull: true,
      comment: 'PostgreSQL vector类型存储',
    };
  } else {
    schema.embedding = {
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
    };
  }

  const model = sequelize.define('Image', schema);

  if (isPostgres) {
    model.prototype.getEmbedding = function () {
      const value = this.embedding;
      return value ? JSON.parse(value) : null;
    };

    model.prototype.setEmbedding = function (value) {
      this.embedding = value ? JSON.stringify(value) : null;
      return this;
    };

    model.prototype.getEmbeddingVector = function () {
      return this.embeddingVector;
    };

    model.prototype.setEmbeddingVector = function (value) {
      this.embeddingVector = value;
      return this;
    };
  }

  return model;
};

module.exports = Image;
